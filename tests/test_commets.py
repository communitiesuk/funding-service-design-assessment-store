"""
Test magic links functionality
"""
import pytest
from tests.mocks.sqlite_test_db import SqliteTestDB


@pytest.mark.usefixtures("flask_test_client")
class TestCommentsEndpoint:
    assessment_id = str(SqliteTestDB.assessment_2_uuid)
    sub_criteria_id = str(SqliteTestDB.sub_crit_2_uuid)
   
    def test_comments_endpoints(self, flask_test_client):
        
        #---------- POST endpoint ----------#
        """
        GIVEN a running Flask client and db
        WHEN we post to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/comments
        THEN a comment is posted/created.
        :param flask_test_client:
        """
        post_endpoint = (
        f"/assessments/{self.assessment_id}/sub_criterias/{self.sub_criteria_id}/comments"
        )
        post_comment_body = {
            "comment": "Gio is the best",
            "assessor_user_id": "1212-22-Gio"
        }
    
        post_response = flask_test_client.post(post_endpoint, json=post_comment_body)
        created_comment = post_response.get_json()
        assess_id = created_comment['assessment_id']
        sub_id = created_comment['sub_criteria_id']
        created_at = created_comment['created_at']
        comment_id = created_comment['id']
     
        assert post_response.status_code == 201
        assert (
            created_comment["comment"]
            == post_comment_body['comment']
        )
        
         #---------- GET endpoint ----------#
        """
        GIVEN a running Flask client and db
        WHEN we get to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/comments
        THEN a list of comments is returned.
        :param flask_test_client:
        """
        
        get_endpoint = (
        f"/assessments/{assess_id}/sub_criterias/{sub_id}/comments"
        )
        
        expected_comment_body = {'assessment_id': assess_id, 'assessor_user_id': '1212-22-Gio', 'comment': 'Gio is the best', 'comment_id': comment_id, 'created_at': created_at, 'sub_criteria_id': sub_id}
        
        get_response = flask_test_client.get(get_endpoint)
        get_comment = get_response.get_json()
        assert get_response.status_code == 200
        assert get_comment['comments'][0] == expected_comment_body
       