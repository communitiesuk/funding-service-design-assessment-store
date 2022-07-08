from typing import List

from db.models.assessment import Assessment
from db.models.comments import Comments
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


def comments_response(comments: Comments, code: int = 200):
    return (
        make_response(
            {
                "comments_id": comments.comments_id,
                "created_at": comments.created_at,
                "comment": comments.comment,
                "sub_criteria_id": comments.sub_criteria_id,
                "assessment_id": comments.assessment_id,
            }
        ),
        code,
    )


def comments_response_list(
    comments_justifications_list: List[Comments], code: int = 200
):
    return (
        make_response(
            {
                "comments": [
                    {
                        "comments_id": comments.comments_id,
                        "created_at": comments.created_at,
                        "comment": comments.comment,
                        "sub_criteria_id": comments.sub_criteria_id,
                        "assessment_id": comments.assessment_id,
                    }
                    for comments in comments_justifications_list
                ]
            }
        ),
        code,
    )
