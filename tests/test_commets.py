"""
Test magic links functionality
"""
import pytest
from tests.mocks.sqlite_test_db import SqliteTestDB


@pytest.mark.usefixtures("flask_test_client")
class TestCommentsEndpoint:
    

    assessment_id = str(SqliteTestDB.assessment_2_uuid)
    sub_criteria_id = str(SqliteTestDB.sub_crit_2_uuid)
    comment = str(SqliteTestDB.comment_1)
    endpoint = (
        f"/assessments/{assessment_id}/sub_criterias/{sub_criteria_id}/comments"
    )


    # def test_get_comments_list(self, flask_test_client):
    #     expected_comment_list = [
    #         {
    #             "id": str(SqliteTestDB.comment_1),  # noqa
    #             "created_at": "2022-07-07T09:11:38.240578Z",
    #             "sub_criteria_id": str(SqliteTestDB.sub_crit_2_uuid),
    #             "assessment_id": str(SqliteTestDB.assessment_2_uuid),
    #             "comment": "wow",
    #             "assessor_user_id": "rio",
    #         }
    #     ]
    #     response = flask_test_client.get(self.endpoint)
    #     get_comment = response.get_json()

    #     assert response.status_code == 200
       

   
    def test_post_comments(self, flask_test_client):
        body = {
            "comment": " Gio is the best",
            "assessor_user_id": "1212-22-Gio"
        }
        response = flask_test_client.post(self.endpoint, json=body)
        created_comment = response.get_json()
        assert response.status_code == 201
        print(created_comment)
        assert (
            created_comment["comment"]
            == body['comment']
        )
