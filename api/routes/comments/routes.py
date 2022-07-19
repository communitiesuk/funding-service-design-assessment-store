from sqlite3 import IntegrityError

import db
from api.responses import comments_list_response
from api.responses import error_response
from db.models.comments import Comments
from flask.views import MethodView


class CommentsView(MethodView):
    def post(sub_criteria_id: str, assessment_id: str, body: dict):

        assessor_user_id = body.get("assessor_user_id")
        comment = body.get("comment")

        new_comment = Comments(
            assessment_id=assessment_id,
            sub_criteria_id=sub_criteria_id,
            assessor_user_id=assessor_user_id,
            comment=comment,
        )

        try:
            db.session.add(new_comment)
            db.session.commit()
        except IntegrityError:
            return error_response(500, "DB Integrity error.")

    def get(sub_criteria_id: str, assessment_id: str):

        comments_list = (
            db.session.query(Comments)
            .filter(
                Comments.assessment_id == assessment_id,
                Comments.sub_criteria_id == sub_criteria_id,
            )
            .all()
        )

        return comments_list_response(comments_list)
