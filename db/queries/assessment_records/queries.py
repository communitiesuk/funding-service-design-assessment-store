"""Queries which are performed on the `assessment_records` table.

Joins allowed.
"""
import json
from datetime import datetime
from typing import Dict
from typing import List

from db import db
from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record import TagAssociation
from db.models.assessment_record.enums import Status
from db.models.flags.flag_update import FlagStatus
from db.models.score import Score
from db.models.tag.tag_types import TagType
from db.models.tag.tags import Tag
from db.queries.assessment_records._helpers import derive_application_values
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
from sqlalchemy.orm import load_only


def get_metadata_for_application(
    application_id: str,
) -> List[Dict]:
    statement = (
        select(AssessmentRecord)
        .options(defer(AssessmentRecord.jsonb_blob))
        .where(AssessmentRecord.application_id == application_id)
    )

    result = db.session.scalar(statement)
    metadata_serializer = AssessmentRecordMetadata(
        exclude=("jsonb_blob", "application_json_md5")
    )
    return metadata_serializer.dump(result)


def get_metadata_for_fund_round_id(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    asset_type: str = "",
    status: str = "",
    search_in: str = "",
    funding_type: str = "",
    countries: List[str] = ["all"],
    filter_by_tag: str = "",
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

    if filter_by_tag and filter_by_tag.casefold() != "all":
        assessment_records_by_tag_id = (
            db.session.query(AssessmentRecord)
            .join(TagAssociation)
            .filter(TagAssociation.tag_id == filter_by_tag)
            .filter(TagAssociation.associated == True)  # noqa E712
            .all()
        )
        record_ids_with_tag_id = [
            record.application_id for record in assessment_records_by_tag_id
        ]
        statement = statement.where(
            AssessmentRecord.application_id.in_(record_ids_with_tag_id)
        )

    if "all" not in countries:
        current_app.logger.info(
            f"Performing assessment search on countries: {countries}."
        )
        statement = statement.where(
            AssessmentRecord.location_json_blob["country"].astext.ilike(
                func.any_(countries)
            )
        )

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

    assessment_metadatas = db.session.scalars(statement).all()

    if status != "ALL":
        filter_assessments = []
        for assessment in assessment_metadatas:

            all_latest_status = [
                flag.latest_status for flag in assessment.flags
            ]
            is_qa_complete = True if assessment.qa_complete else False

            if FlagStatus.STOPPED in all_latest_status:
                display_status = "STOPPED"
            elif all_latest_status.count(FlagStatus.RAISED) > 1:
                display_status = "MULTIPLE_FLAGS"
            elif all_latest_status.count(FlagStatus.RAISED) == 1:
                display_status = "FLAGGED"
            elif is_qa_complete:
                display_status = "QA_COMPLETED"
            else:
                display_status = assessment.workflow_status.name

            if display_status == status:
                filter_assessments.append(assessment)

        assessment_metadatas = filter_assessments

    metadata_serialiser = AssessmentRecordMetadata(
        exclude=("jsonb_blob", "application_json_md5")
    )

    assessment_metadatas = [
        metadata_serialiser.dump(app_metadata)
        | {"is_qa_complete": True if app_metadata.qa_complete else False}
        for app_metadata in assessment_metadatas
    ]

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


def get_assessment_records_by_round_id(
    round_id, selected_fields=None, language=None
):  # noqa
    """
    Retrieve the latest scores and associated information for each subcriteria
    of AssessmentRecords matching the given round_id.

    Parameters:
        round_id (UUID): The ID of the round to filter AssessmentRecords.

    Returns:
        list: A list of dictionaries, each containing the latest score and its associated
        information for each subcriteria of the AssessmentRecords that match the given round_id.
    """
    default_fields = [
        "Application ID",
        "Short ID",
        "Score Subcriteria",
        "Score",
        "Score Justification",
        "Score Date",
        "Score Time",
    ]

    # If selected_fields is not provided, use the default_fields.
    if selected_fields is None:
        selected_fields = default_fields

    selected_fields = [
        field for field in selected_fields if field in default_fields
    ]
    subquery = (
        db.session.query(
            Score.application_id,
            Score.sub_criteria_id,
            func.max(Score.date_created).label("latest_date_created"),
        )
        .group_by(Score.application_id, Score.sub_criteria_id)
        .subquery()
    )

    query = (
        db.session.query(Score)
        .join(
            subquery,
            and_(
                Score.application_id == subquery.c.application_id,
                Score.sub_criteria_id == subquery.c.sub_criteria_id,
                Score.date_created == subquery.c.latest_date_created,
            ),
        )
        .join(
            AssessmentRecord,
            Score.application_id == AssessmentRecord.application_id,
        )
        .filter(AssessmentRecord.round_id == round_id)
    )

    if language is not None:
        query = query.filter(AssessmentRecord.language == language)

    latest_scores = query.all()

    output = []
    for score in latest_scores:

        score_data = {
            "Application ID": score.application_id,
            "Short ID": AssessmentRecord.query.get(
                score.application_id
            ).short_id,
            "Score Subcriteria": score.sub_criteria_id,
            "Score": score.score,
            "Score Justification": score.justification,
            "Score Date": score.date_created.strftime("%d/%m/%Y"),
            "Score Time": score.date_created.strftime("%H:%M:%S"),
        }

        selected_score_data = {
            field: score_data[field] for field in selected_fields
        }
        output.append(selected_score_data)
    return output


def associate_assessment_tags(application_id, tags: List):
    existing_associated_tags = TagAssociation.query.filter(
        TagAssociation.application_id == application_id,
        TagAssociation.associated == True,  # noqa: E712
    ).all()

    # Create a dictionary to quickly lookup existing tags by tag_id
    existing_associated_tags_dict = {
        str(tag.tag_id): tag for tag in existing_associated_tags
    }

    # Iterate over the provided tags and update the tag associations
    for tag in tags:
        tag_id = tag.get("id")
        user_id = tag.get("user_id")
        associated = True  # Set associated value to True for provided tags

        # Check if the tag already exists in the database
        if tag_id not in existing_associated_tags_dict:
            new_tag = TagAssociation(
                application_id=application_id,
                tag_id=tag_id,
                associated=associated,
                user_id=user_id,
            )
            db.session.add(new_tag)

    # Dis-associate any existing tags that are not present in the provided list
    incoming_tag_ids = {tag["id"] for tag in tags}
    for tag in existing_associated_tags:
        if str(tag.tag_id) not in incoming_tag_ids:
            tag.associated = False

    db.session.commit()

    # Return the updated tag associations
    updated_tags = TagAssociation.query.filter(
        TagAssociation.application_id == application_id,
        TagAssociation.associated == True,  # noqa: E712
    ).all()
    return updated_tags


def select_active_tags_associated_with_assessment(application_id):

    tag_associations = (
        db.session.query(
            Tag.id.label("tag_id"),
            Tag.value,
            TagType.purpose,
            TagType.description,
            TagAssociation.associated,
            TagAssociation.user_id,
            AssessmentRecord.application_id,
        )
        .join(
            AssessmentRecord,
            TagAssociation.application_id == AssessmentRecord.application_id,
        )
        .join(Tag, Tag.id == TagAssociation.tag_id)
        .join(TagType, Tag.type_id == TagType.id)
        .filter(AssessmentRecord.application_id == application_id)
        .filter(TagAssociation.associated == True)  # noqa: E712
        .filter(Tag.active == True)  # noqa: E712
        .all()
    )

    db.session.commit()
    return tag_associations


def get_assessment_export_data(
    fund_id: str, round_id: str, report_type: str, list_of_fields: dict
):
    en_statement = select(AssessmentRecord).where(
        AssessmentRecord.fund_id == fund_id,
        AssessmentRecord.round_id == round_id,
        AssessmentRecord.language == "en",
    )

    en_assessment_metadatas = db.session.scalars(en_statement).all()

    cy_statement = select(AssessmentRecord).where(
        AssessmentRecord.fund_id == fund_id,
        AssessmentRecord.round_id == round_id,
        AssessmentRecord.language == "cy",
    )

    cy_assessment_metadatas = db.session.scalars(cy_statement).all()

    en_list = get_export_data(
        round_id=round_id,
        report_type=report_type,
        list_of_fields=list_of_fields,
        assessment_metadatas=en_assessment_metadatas,
        language="en",
    )
    cy_list = get_export_data(
        round_id=round_id,
        report_type=report_type,
        list_of_fields=list_of_fields,
        assessment_metadatas=cy_assessment_metadatas,
        language="cy",
    )

    obj = {"en_list": en_list, "cy_list": cy_list}
    return obj


def get_export_data(
    round_id: str,
    report_type: str,
    list_of_fields: dict,
    assessment_metadatas: list,
    language: str,  # noqa
) -> List[Dict]:  # noqa

    form_fields = list_of_fields[report_type].get("form_fields", {})
    field_ids = form_fields.keys()
    finalList = []

    if len(form_fields) != 0:
        for assessment in assessment_metadatas:

            iso_format = "%Y-%m-%dT%H:%M:%S.%f"
            iso_datetime = datetime.strptime(
                assessment.jsonb_blob["date_submitted"], iso_format
            )
            formatted_date = iso_datetime.strftime("%d/%m/%Y %H:%M:%S")

            applicant_info = {
                "Application ID": assessment.application_id,
                "Short ID": assessment.short_id,
                "Date Submitted": formatted_date,
            }
            forms = assessment.jsonb_blob["forms"]
            for form in forms:
                questions = form["questions"]
                for question in questions:
                    fields = question["fields"]
                    for field in fields:
                        if field["key"] in field_ids:
                            title = form_fields[field["key"]][language][
                                "title"
                            ]
                            applicant_info[title] = field["answer"]
            applicant_info = add_missing_elements_with_empty_values(
                applicant_info, form_fields, language
            )
            finalList.append(applicant_info)

    output = {}
    if report_type == "OUTPUT_TRACKER":
        output = get_assessment_records_by_round_id(
            round_id,
            list_of_fields[report_type].get("score_fields", None),
            language,
        )
        if len(output) != 0:
            finalList = combine_dicts(finalList, output)

    return finalList


# adds miissing elements for use in the csv
def add_missing_elements_with_empty_values(
    applicant_info, form_fields, language
):
    result_data = applicant_info.copy()

    for key, value in form_fields.items():
        title = value[language]["title"]
        if title not in result_data:
            result_data[title] = ""
    return result_data


def combine_dicts(applications_list, scores_list):
    combined_list = []

    if len(applications_list) == 0 and len(scores_list) == 0:
        return combined_list
    if len(applications_list) == 0:
        return scores_list
    if len(scores_list) == 0:
        return applications_list

    for application in applications_list:
        app_id = application["Application ID"]
        matching_scores = [
            score for score in scores_list if score["Application ID"] == app_id
        ]

        for score in matching_scores:
            combined_element = {**application, **score}
            combined_list.append(combined_element)

    return combined_list
