from api.responses import comments_response
from api.responses import comments_response_list
from api.responses import error_response
from db.models.comments import CommentsError
from db.models.comments import CommentsMethods
from flask import request
from flask.views import MethodView


class CommentsView(CommentsMethods, MethodView):
    def get(self):
        """
        GET /assessments/{assessment_id}/sub_criterias/
                {sub_criteria_id}/comment endpoint
        return comments for the sub_criteria for the assessment
        If no matching valid link is found returns a 404 error message
        :param assessment_id: id of the assessment
        :param sub_criteria_id: id of the sub_criteria
        :return: 200 assessment JSON / 404 Error
        """
        json = request.get_json()
        assessment_id = json.get("assessment_id")
        sub_criteria_id = json.get("sub_criteria_id")

        try:
            comments_list = self.comment(assessment_id, sub_criteria_id)
        except CommentsError as e:
            return error_response(404, e.message)

        return comments_response_list(comments_list)

    def post(self):
        """
        Adss a comment for a subcriteria
        :param assessment_id: ID of assessment
        :param sub_criteria_id: ID of sub-criteria
        :param person_id: person's ID who provides the score and justification
        :param comment: Comment for teh sub-criteria
        :return: a json of the comment created (or an error if failure)
        """
        json = request.get_json()
        assessment_id = json.get("assessment_id")
        sub_criteria_id = json.get("sub_criteria_id")
        person_id = json.get("person_id")
        comment = json.get("comment")

        try:
            new_comment = self.comments(
                assessment_id, sub_criteria_id, person_id, comment
            )
        except CommentsError as e:
            return error_response(401, e.message)

        return comments_response(new_comment, 201)
