"""Queries which are performed on the `assessment_records` table.

Joins allowed.
"""
import json
from typing import Dict
from typing import List

from db import db
from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record import TagAllocation
from db.models.assessment_record.enums import Status
from db.models.flags import Flag
from db.models.flags.enums import FlagType
from db.queries.assessment_records._helpers import derive_application_values
from db.queries.flags.queries import find_qa_complete_flags
from db.schemas import AssessmentRecordMetadata
from db.schemas import AssessmentSubCriteriaMetadata
from db.schemas import AssessorTaskListMetadata
from flask import current_app
from sqlalchemy import and_
from sqlalchemy import bindparam
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.orm import defer
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import load_only


def get_metadata_for_fund_round_id(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    asset_type: str = "",
    status: str = "",
    search_in: str = "",
    funding_type: str = "",
) -> List[Dict]:
    """get_metadata_for_fund_round_id Executes a query on assessment records
    which returns all rows matching the given fund_id and round_id. Has
    optional parameters of search_term, asset_type and status for filterting.
    Excludes irrelevant columns such as
    `db.models.AssessmentRecord.jsonb_blob`.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.
    """

    statement = (
        select(AssessmentRecord)
        # Dont load json into memory
        .options(defer(AssessmentRecord.jsonb_blob)).where(
            AssessmentRecord.fund_id == fund_id,
            AssessmentRecord.round_id == round_id,
        )
    )
    if search_term != "":
        current_app.logger.info(
            f"Performing assessment search on search term: {search_term} in fields {search_in}"
        )
        search_term = search_term.replace(" ", "%")

        filters = []
        if "short_id" in search_in:
            filters.append(AssessmentRecord.short_id.ilike(f"%{search_term}%"))
        if "project_name" in search_in:
            filters.append(
                AssessmentRecord.project_name.ilike(f"%{search_term}%")
            )
        if "organisation_name" in search_in:
            filters.append(
                func.cast(AssessmentRecord.organisation_name, String).ilike(
                    f"%{search_term}%"
                )
            )

        statement = statement.filter(or_(*filters))

    if asset_type != "ALL" and asset_type != "":
        current_app.logger.info(
            f"Performing assessment search on asset type: {asset_type}."
        )
        statement = statement.where(AssessmentRecord.asset_type == asset_type)

    if funding_type != "ALL" and funding_type != "":
        current_app.logger.info(
            f"Performing assessment search on funding type: {funding_type}."
        )
        # TODO SS figure out how to stop double quoting this - it works but is ugly
        # it's because when we retrieve the json element as funding_type, we get it as a json element, not pure text,
        # so it has the double quotes from the json so we have to include them in the comparison
        statement = statement.where(
            func.cast(AssessmentRecord.funding_type, String)
            == f'"{funding_type}"'
        )

    match status:
        case FlagType.QA_COMPLETED.name:
            current_app.logger.info(
                f"Performing search for assessments with flag: {status}."
            )
            statement = (
                statement.join(Flag)
                .group_by(AssessmentRecord.application_id)
                .filter(Flag.flag_type == status)
            )

        case (  # noqa
            Status.NOT_STARTED.name
            | Status.IN_PROGRESS.name
            | Status.COMPLETED.name
        ):
            current_app.logger.info(
                f"Performing search for assessments with status: {status}."
            )
            statement = statement.where(
                AssessmentRecord.workflow_status == status
            )

        case FlagType.STOPPED.name | FlagType.FLAGGED.name:
            # Only keep assessment records whoms most recent
            #  flag matches the status parameter.
            current_app.logger.info(
                "Performing search for assessments with"
                f" latest flag: {status}."
            )
            subq = (
                db.session.query(
                    Flag.application_id,
                    func.max(Flag.date_created).label("maxdate"),
                )
                .group_by(Flag.application_id)
                .subquery("t2")
            )

            query = db.session.query(Flag.application_id).join(
                subq,
                and_(
                    Flag.application_id == subq.c.application_id,
                    Flag.date_created == subq.c.maxdate,
                    Flag.flag_type == status,
                ),
            )
            applications_with_latest_flag_match = [
                x.application_id for x in db.session.execute(query).all()
            ]

            statement = statement.filter(
                AssessmentRecord.application_id.in_(
                    applications_with_latest_flag_match
                )
            )

    assessment_metadatas = db.session.scalars(statement).all()
    metadata_serialiser = AssessmentRecordMetadata(
        exclude=("jsonb_blob", "application_json_md5")
    )

    app_ids = {
        app_metadata.application_id for app_metadata in assessment_metadatas
    }
    app_id_is_qa_complete_dict = find_qa_complete_flags(app_ids)
    assessment_metadatas = [
        metadata_serialiser.dump(app_metadata)
        | {
            "is_qa_complete": app_id_is_qa_complete_dict[
                app_metadata.application_id
            ]
        }
        for app_metadata in assessment_metadatas
    ]

    def sort_flags_in_assessment_records(
        assessment_records, sort_field, sort_order
    ):
        """Sorts flag data in assessment_records in the provided sort order."""
        sort_key = lambda x: x[sort_field]  # noqa E731
        reverse = sort_order != "asc"
        for record in assessment_records:
            record["flags"] = sorted(
                record["flags"], key=sort_key, reverse=reverse
            )

        return assessment_records

    assessment_metadatas = sort_flags_in_assessment_records(
        assessment_metadatas, sort_field="date_created", sort_order="asc"
    )

    return assessment_metadatas


def bulk_insert_application_record(
    application_json_strings: List[str], application_type: str, is_json=False
) -> List[AssessmentRecord]:
    """bulk_insert_application_record Given a list of json strings
    and an `application_type` we extract key values from the json
    strings before inserting them with the remaining values into
    `db.models.AssessmentRecord`.

    :param application_json_strings: _description_
    :param application_type: _description_
    """
    print("Beginning bulk application insert.")
    rows = []
    if len(application_json_strings) < 1:
        print(
            f"No new submitted applications found for {application_type}. skipping Import..."
        )
        return rows
    print("\n")
    # Create a list of application ids to track inserted rows
    for single_application_json in application_json_strings:
        if not is_json:
            single_application_json = json.loads(single_application_json)

        derived_values = derive_application_values(single_application_json)

        row = {
            **derived_values,
            "jsonb_blob": single_application_json,
            "type_of_application": application_type,
        }
        try:
            stmt = postgres_insert(AssessmentRecord).values([row])

            upsert_rows_stmt = stmt.on_conflict_do_nothing(
                index_elements=[AssessmentRecord.application_id]
            ).returning(AssessmentRecord.application_id)

            print(f"Attempting insert of application {row['application_id']}")
            result = db.session.execute(upsert_rows_stmt)

            # Check if the inserted application is in result
            inserted_application_ids = [item.application_id for item in result]
            if not len(inserted_application_ids):
                print(
                    f"Application id already exist in the database: {row['application_id']}"
                )
            else:
                rows.append(row)
            db.session.commit()
            del single_application_json
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            print(
                f"Error occurred while inserting application {row['application_id']}, error: {e}"
            )

    print(
        "Inserted application_ids (i.e. application rows) :"
        f" {[row['application_id'] for row in rows]}"
    )
    return rows


def delete_assessment_record(app_id):
    """
    Delete the assessment record with the given ID from the database.
    Returns True if the record was successfully deleted, or False otherwise.
    """
    try:
        assessment_record = AssessmentRecord.query.get(app_id)
        if assessment_record is not None:
            db.session.delete(assessment_record)
            db.session.commit()
            return True
    except Exception as e:
        print(f"Error deleting assessment record: {e}")
    return False


def find_answer_by_key_runner(field_key: str, app_id: str) -> List[tuple]:
    """find_answer_by_key_runner Given an application id `app_id` and a field
    to search for `app_id` we return the matching field object (A json with
    keys {key, answer, title, type}) within an SQLAlchemy result.

    :param field_key: The unique key of the field.
    :type field_key: str
    :param app_id: The application id of the queried row.
    :type app_id: str
    :return: The whole field object of the found field. Returned as a
    SQLAlchemy result.
    :rtype: List[tuple]
    """

    return (
        db.session.query(
            func.jsonb_path_query_first(
                AssessmentRecord.jsonb_blob,
                "$.forms[*].questions[*].fields[*] ? (@.key =="
                f' "{field_key}")',
            )
        )
        .filter(AssessmentRecord.application_id == app_id)
        .one()
    )


def find_assessor_task_list_state(application_id: str) -> dict:
    """find_assessment Given an application id `application_id` we return the
    matching row from the `assessment_records` table.

    :param application_id: The application id of the queried row.
    :type application_id: str
    :return: The matching row from the `assessment_records` table.
    :rtype: dict
    """

    stmt = (
        select(AssessmentRecord)
        .where(AssessmentRecord.application_id == application_id)
        .options(
            load_only(
                "short_id",
                "project_name",
                "workflow_status",
                "jsonb_blob",
                "fund_id",
                "round_id",
                "funding_amount_requested",
            )
        )
    )

    assessment_record = db.session.scalar(stmt)

    assessment_record_json = AssessorTaskListMetadata(
        only=(
            "short_id",
            "project_name",
            "date_submitted",
            "workflow_status",
            "fund_id",
            "round_id",
            "funding_amount_requested",
        )
    ).dump(assessment_record)

    return assessment_record_json


def get_assessment_sub_critera_state(application_id: str) -> dict:
    """Given an application id `application_id` we return the
    relevant record from the `assessment_records` table with
    state related to the assessments sub_criteria context.

    :param application_id: The application id of the queried row.
    :type application_id: str
    :return: The matching row from the `assessment_records` table.
    :rtype: dict
    """

    stmt = (
        select(AssessmentRecord)
        .where(AssessmentRecord.application_id == application_id)
        .options(
            load_only(
                "funding_amount_requested",
                "project_name",
                "fund_id",
                "workflow_status",
                "short_id",
            )
        )
    )

    assessment_record = db.session.scalar(stmt)

    assessment_record_json = AssessmentSubCriteriaMetadata(
        only=(
            "funding_amount_requested",
            "project_name",
            "fund_id",
            "workflow_status",
            "short_id",
        )
    ).dump(assessment_record)

    return assessment_record_json


def get_application_jsonb_blob(application_id: str) -> dict:
    stmt = (
        select(AssessmentRecord)
        .where(AssessmentRecord.application_id == application_id)
        .options(load_only("jsonb_blob"))
    )
    application_jsonb_blob = db.session.scalar(stmt)
    application_json = AssessorTaskListMetadata().dump(application_jsonb_blob)
    return application_json


def bulk_update_location_jsonb_blob(application_ids_to_location_data):
    stmt = (
        update(AssessmentRecord)
        .where(AssessmentRecord.application_id == bindparam("app_id"))
        .values(location_json_blob=bindparam("location_data"))
    )

    for item in application_ids_to_location_data:
        existing_location_data = (
            db.session.query(AssessmentRecord.location_json_blob)
            .filter_by(application_id=item["application_id"])
            .scalar()
        )

        if not existing_location_data:
            print("Seeding location data")
            db.session.execute(
                stmt,
                {
                    "app_id": item["application_id"],
                    "location_data": item["location"],
                },
            )

        elif existing_location_data["error"] is True:
            print("Updating location data")
            db.session.execute(
                stmt,
                {
                    "app_id": item["application_id"],
                    "location_data": item["location"],
                },
            )

        else:
            print("Location data already exists")
            continue

    db.session.commit()


def update_status_to_completed(application_id):
    current_app.logger.info(
        "Updating application status to COMPLETED"
        f" for application: {application_id}."
    )
    db.session.query(AssessmentRecord).filter(
        AssessmentRecord.application_id == application_id
    ).update(
        {AssessmentRecord.workflow_status: Status.COMPLETED},
        synchronize_session=False,
    )

    db.session.commit()


def get_assessment_records_by_round_id(round_id):
    """
    Retrieves assessment records and scores based on the provided round ID.

    Parameters:
    - round_id: Short identification code used to query assessment records.

    Returns:
    - List of dictionaries containing relevant information extracted from assessment records and scores.
    Each dictionary represents a record and includes the following fields:

        - "Short id": Short identification code of the assessment record.
        - "Application ID": Identification of the associated application.
        - "Score Subcriteria": ID of the score subcriteria.
        - "Score": Score assigned to the subcriteria.
        - "Score Justification": Justification for the assigned score.
        - "Score Date Created": Date when the score was created.
    """
    # Query assessment records and scores
    assessment_records = (
        AssessmentRecord.query.filter(AssessmentRecord.round_id == round_id)
        .options(joinedload(AssessmentRecord.scores))
        .all()
    )

    # Extract relevant information and format the output
    output = []
    for record in assessment_records:
        for score in record.scores:
            output.append(
                {
                    "Short id": record.short_id,
                    "Application ID": record.application_id,
                    "Score Subcriteria": score.sub_criteria_id,
                    "Score": score.score,
                    "Score Justification": score.justification,
                    "Score Date Created": score.date_created,
                }
            )

    return output


def set_tags_for_assessment(application_id, new_tags):
    stmt = select(TagAllocation).where(
        TagAllocation.application_id == application_id
    )
    existing_tags = db.session.scalars(stmt).all()
    for tag in existing_tags:
        if tag.tag_value not in new_tags:
            db.session.delete(tag)

    if len(new_tags) > 0:
        tag_inserts = [
            {"application_id": application_id, "tag_value": tag_value}
            for tag_value in new_tags
        ]
        db.session.execute(
            postgres_insert(TagAllocation)
            .values(tag_inserts)
            .on_conflict_do_nothing()
        )
    db.session.commit()
