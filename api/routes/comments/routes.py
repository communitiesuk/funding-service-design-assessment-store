from api.responses import comments_list_response, created_comment_response
from api.responses import error_response
from db.models.comments import  CommentsError, CommentsMethods
from flask.views import MethodView


class CommentsView(CommentsMethods, MethodView):

    def get(self, assessment_id: str, sub_criteria_id: str):
    
        try:
            comments_list = self.comments_list(
                 assessment_id= assessment_id, sub_criteria_id= sub_criteria_id
            )
        except CommentsError as e:
            return error_response(404, e.message)

        return comments_list_response(comments_list)
    

    def post(self, sub_criteria_id: str, assessment_id: str, body: dict):

        assessor_user_id = body.get("assessor_user_id")
        comment = body.get("comment")

        try: 
            new_comment = self.create_comment(
                assessment_id=assessment_id,
                sub_criteria_id=sub_criteria_id,
                assessor_user_id=assessor_user_id,
                comment=comment,
            )
        except CommentsError as e:
            return error_response(401, e.message)
        
        return created_comment_response(new_comment, 201)
