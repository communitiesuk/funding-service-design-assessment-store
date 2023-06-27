# flake8: noqa
import json
from copy import deepcopy
from typing import Dict
from typing import List

from api.models.sub_criteria import SubCriteria
from api.routes._helpers import transform_to_assessor_task_list_metadata
from api.routes.subcriterias.get_sub_criteria import (
    map_application_with_sub_criteria_themes,
)
from api.routes.subcriterias.get_sub_criteria import (
    return_subcriteria_from_mapping,
)
from db.queries import get_metadata_for_fund_round_id
from db.queries.assessment_records.queries import find_assessor_task_list_state
from db.queries.assessment_records.queries import get_application_jsonb_blob
from db.queries.assessment_records.queries import (
    get_assessment_sub_critera_state,
)
from db.queries.assessment_records.queries import update_status_to_completed
from db.queries.comments.queries import get_sub_criteria_to_has_comment_map
from db.queries.flags.queries import find_qa_complete_flag_for_applications
from db.queries.flags.queries import get_latest_flags_for_each
from db.queries.scores.queries import get_sub_criteria_to_latest_score_map
from flask import current_app

with open("s41-dummy-json/all_assessments_for_fund_round.json", "r") as f:
    static_response_data_s41 = json.load(f)
COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"

NSTF_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NSTF_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"


def all_assessments_for_fund_round_id(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    asset_type: str = "ALL",
    status: str = "ALL",
) -> List[Dict]:
    """all_assessments_for_fund_round_id Function used by the endpoint
    `/application_overviews/{fund_id}/{round_id}`.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.
    """

    this_response = deepcopy(static_response_data_s41)
    if fund_id == NSTF_FUND_ID:
        for application in this_response:
            application["fund_id"] = NSTF_FUND_ID
            application["round_id"] = NSTF_ROUND_2_ID
            application["type_of_application"] = "NSTF"
            sr = application["short_id"]
            application["short_id"] = sr.replace("COF", "NSTF").replace(
                "R2W3", "R2"
            )

    return this_response

    app_list = get_metadata_for_fund_round_id(
        fund_id=fund_id,
        round_id=round_id,
        search_term=search_term,
        asset_type=asset_type,
        status=status,
    )
    return app_list


def sub_criteria(
    application_id: str,
    sub_criteria_id: str,
) -> Dict:
    """Returns metadata and themes for a sub_criteria
    `/sub_criteria_overview/{sub_criteria_id}`.

    :param sub_criteria_id: The stringified sub criteria id (NOT sub critria name).
    :return: A sub criteria dictionary.
    """
    current_app.logger.info(
        "Processing request for sub criteria: {sub_criteria_id}."
    )
    metadata = find_assessor_task_list_state(application_id)
    current_app.logger.info(
        "Searching assessment mapping for sub criteria: {sub_criteria_id}."
    )
    sub_criteria_config_from_mapping = return_subcriteria_from_mapping(
        sub_criteria_id, metadata["fund_id"], metadata["round_id"]
    )
    current_app.logger.info(
        "Getting application subcriteria metadata for application: {sub_criteria_id}."
    )
    application_metadata_for_subcriteria = get_assessment_sub_critera_state(
        application_id
    )
    sub_criteria = SubCriteria.from_filtered_dict(
        {
            **sub_criteria_config_from_mapping,
            **application_metadata_for_subcriteria,
        }
    )
    sub_criteria_dict = sub_criteria.to_dict()
    return sub_criteria_dict


def get_banner_state(application_id: str) -> dict:
    return get_assessment_sub_critera_state(application_id)


def get_assessor_task_list_state(application_id: str) -> dict:
    """get_assessor_task_list_state Function used by the endpoint
    `/assessor_task_list/{application_id}`.

    :param application_id: The stringified application UUID.
    :return: A dictionary.
    """

    metadata = find_assessor_task_list_state(application_id)
    score_map = get_sub_criteria_to_latest_score_map(application_id)
    comment_map = get_sub_criteria_to_has_comment_map(application_id)
    sections, criterias = transform_to_assessor_task_list_metadata(
        metadata["fund_id"], metadata["round_id"], score_map, comment_map
    )

    metadata["sections"] = sections
    metadata["criterias"] = criterias

    return metadata


def get_sub_criteria_theme_answers(application_id: str, theme_id: str):
    """Function returns mapped answers from application & Sub_criteria_themes
    with given application_id and theme_id"""
    metadata = find_assessor_task_list_state(application_id)
    return map_application_with_sub_criteria_themes(
        application_id, theme_id, metadata["fund_id"], metadata["round_id"]
    )


def update_ar_status_to_completed(application_id: str):
    """Function updates the status to COMPLETE for the given application_id"""
    update_status_to_completed(application_id)


def assessment_stats_for_fund_round_id(
    fund_id: str,
    round_id: str,
    search_term: str = "",
    asset_type: str = "ALL",
    status: str = "ALL",
) -> List[Dict]:
    """
    Function used by the endpoint
    `/assessments/get-stats/{fund_id}/{round_id}`
    that returns a dictionary of metrics about
    assessments for a given fund_id and round_id.

    :param fund_id: The stringified fund UUID.
    :param round_id: The stringified round UUID.
    :return: A list of dictionaries.
    """
    stats = {}
    assessments = get_metadata_for_fund_round_id(
        fund_id=fund_id,
        round_id=round_id,
        search_term=search_term,
        asset_type=asset_type,
        status=status,
    )
    assessment_ids = [
        application["application_id"] for application in assessments
    ]

    qa_completed_assessments = [
        flag["application_id"]
        for flag in find_qa_complete_flag_for_applications(assessment_ids)
    ]
    stopped_assessments = [
        flag["application_id"] for flag in get_latest_flags_for_each("STOPPED")
    ]
    flagged_assessments = [
        flag["application_id"] for flag in get_latest_flags_for_each("FLAGGED")
    ]
    stats.update(
        {
            "completed": len(
                [
                    1
                    for assessment in assessments
                    if assessment["workflow_status"] == "COMPLETED"
                ]
            ),
            "assessing": len(
                [
                    1
                    for assessment in assessments
                    if assessment["workflow_status"] == "IN_PROGRESS"
                ]
            ),
            "not_started": len(
                [
                    1
                    for assessment in assessments
                    if assessment["workflow_status"] == "NOT_STARTED"
                ]
            ),
            "qa_completed": len(
                [
                    1
                    for assessment in assessments
                    if assessment["application_id"] in qa_completed_assessments
                ]
            ),
            "stopped": len(
                [
                    1
                    for assessment in assessments
                    if assessment["application_id"] in stopped_assessments
                ]
            ),
            "flagged": len(
                [
                    1
                    for assessment in assessments
                    if assessment["application_id"] in flagged_assessments
                ]
            ),
            "total": len(assessments),
        }
    )

    return stats


def get_application_json(application_id):
    return get_application_jsonb_blob(application_id)
