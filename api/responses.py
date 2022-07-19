# flake8: noqa
from typing import List

from db.models.assessment import Assessment
from db.models.comments import Comments
from db.models.scores_justifications import ScoresJustifications
from db.models.sub_criteria import SubCriteria
from flask import make_response


def error_response(code: int, message: str):
    return (
        make_response({"status": "error", "code": code, "message": message}),
        code,
    )


def assessment_response(assessment: Assessment, code: int = 200):
    return (
        make_response(
            {
                "id": assessment.id,
                "compliance_status": assessment.compliance_status,
                "applicationId": assessment.application_id,
            }
        ),
        code,
    )


def sub_criteria_response(sub_criteria: SubCriteria, code: int = 200):
    return (
        make_response(
            {
                "id": sub_criteria.id,
                "criteria_id": sub_criteria.criteria_id,
                "title": sub_criteria.sub_criteria_title,
            }
        ),
        code,
    )


def scores_justifications_response(
    scores_justifications: ScoresJustifications, code: int = 200
):
    return (
        make_response(
            {
                "id": scores_justifications.id,
                "created_at": scores_justifications.created_at,
                "assessor_user_id": scores_justifications.assessor_user_id,
                "sub_criteria_id": scores_justifications.sub_criteria_id,
                "assessment_id": scores_justifications.assessment_id,
                "score": scores_justifications.score,
                "justification": scores_justifications.justification,
            }
        ),
        code,
    )


def comments_list_response(comments_list: List[Comments], code: int = 200):
    return (
        make_response(
            {
                "comments": [
                    {
                        "user_id": comment.user_id,
                        "created_at": comment.created_at,
                        "assessment_id": comment.assessment_id,
                        "sub_criteria_id": comment.sub_criteria_id,
                        "comment": comment.comment,
                        "comment_id": comment.comment_id,
                    }
                    for comment in comments_list
                ]
            }
        ),
        code,
    )


def scores_justifications_response_list(
    scores_justifications_list: List[ScoresJustifications], code: int = 200
):
    return (
        make_response(
            {
                "scores_justifications": [
                    {
                        "id": scores_justifications.id,
                        "created_at": scores_justifications.created_at,
                        "assessor_user_id": scores_justifications.assessor_user_id,
                        "sub_criteria_id": scores_justifications.sub_criteria_id,
                        "assessment_id": scores_justifications.assessment_id,
                        "score": scores_justifications.score,
                        "justification": scores_justifications.justification,
                    }
                    for scores_justifications in scores_justifications_list
                ]
            }
        ),
        code,
    )
