"""Queries which are performed on the `assessment_records` table.

Joins allowed.
"""
import json
from typing import Dict
from typing import List

from db import db
from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record.enums import Status
from db.queries.assessment_records._helpers import derive_application_values
from db.schemas import AssessmentRecordMetadata
from db.schemas import AssessmentSubCriteriaMetadata
from db.schemas import AssessorTaskListMetadata
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as postgres_insert
from sqlalchemy.orm import defer
from sqlalchemy.orm import load_only


def get_metadata_for_fund_round_id(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    asset_type: str = "",
    status: str = "",
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
        search_term = search_term.replace(" ", "%")
        statement = statement.where(
            AssessmentRecord.short_id.like(f"%{search_term}%")
            | AssessmentRecord.project_name.ilike(f"%{search_term}%")
        )

    if asset_type != "ALL" and asset_type != "":
        statement = statement.where(AssessmentRecord.asset_type == asset_type)

    match status:
        case "NOT_STARTED" | "IN_PROGRESS" | "SUBMITTED" | "COMPLETED":
            statement = statement.where(
                AssessmentRecord.workflow_status == status
            )
        case "INELIGIBLE" | "QA_COMPLETE" | "QA_READY":
            return []  # TODO: Handle these statuses

    assessment_metadatas = db.session.scalars(statement).all()

    application_ids = [a.application_id for a in assessment_metadatas]
    # added locally to avoid circular import
    from db.queries import retrieve_flags_for_applications

    flags = retrieve_flags_for_applications(application_ids)
    flagged_application_ids = [f["application_id"] for f in flags]

    match status:
        case "FLAGGED":
            assessment_metadatas = [
                am
                for am in assessment_metadatas
                if am.application_id in flagged_application_ids
            ]
        case "ALL" | "":
            ...
        case _:
            assessment_metadatas = [
                am
                for am in assessment_metadatas
                if am.application_id not in flagged_application_ids
            ]

    metadata_serialiser = AssessmentRecordMetadata(
        exclude=("jsonb_blob", "application_json_md5")
    )

    assessment_metadatas = [
        metadata_serialiser.dump(app_metadata)
        for app_metadata in assessment_metadatas
    ]

    for am in assessment_metadatas:
        if am["application_id"] in flagged_application_ids:
            am["workflow_status"] = "FLAGGED"

    return assessment_metadatas


def bulk_insert_application_record(
    application_json_strings: List[str], application_type: str, is_json=False
) -> None:
    """bulk_insert_application_record Given a list of json strings
    and an `application_type` we extract key values from the json
    strings before inserting them with the remaining values into
    `db.models.AssessmentRecord`.

    :param application_json_strings: _description_
    :param application_type: _description_
    """
    try:
        print("Beginning bulk application insert.")
        rows = []

        for single_application_json in application_json_strings:
            if not is_json:
                single_application_json = json.loads(single_application_json)

            derived_values = derive_application_values(single_application_json)

            row = {
                **derived_values,
                "jsonb_blob": single_application_json,
                "type_of_application": application_type,
            }
            print(f"Appending row to insert list, values: '{derived_values}'.")
            rows.append(row)

            del single_application_json

        stmt = postgres_insert(AssessmentRecord).values(rows)

        upsert_rows_stmt = stmt.on_conflict_do_nothing(
            index_elements=[AssessmentRecord.application_id]
        )
        print("Attemping bulk insert of all application rows.")
        db.session.execute(upsert_rows_stmt)
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error running bulk insert: '{e.message}'.")
        raise (e)
    db.session.commit()


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


def update_status_to_completed(application_id):
    from flask import current_app
    current_app.logger.error(
             f"Updating application status to COMPLETED")
    db.session.query(AssessmentRecord)\
        .filter(AssessmentRecord.application_id == application_id)\
        .update(
        {AssessmentRecord.workflow_status: Status.COMPLETED}, synchronize_session=False)

    db.session.commit()
    