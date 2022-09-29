"""
Test magic links functionality
"""
from tests.conftest import seeded_assessment_ids
from tests.conftest import seeded_scores_justifications
from tests.conftest import seeded_subcriteria


class TestScoreJustificationEndpoints:
    def test_get_scores_justifications_list(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we get to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/scores
        THEN a list of scores and jsutifications is returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[3].id
        endpoint = (
            f"/assessments/{assessment_id}/"
            f"sub_criterias/{sub_criteria_id}/scores"
        )
        response = client.get(endpoint)
        scores_justifications = response.get_json()

        assert response.status_code == 200
        assert (
            scores_justifications["scores_justifications"][0]
            == seeded_scores_justifications[0].as_json()
        )

    def test_score_justification_is_created(self, client):
        """
        GIVEN a running Flask client and db
        WHEN we POST to /assessments/{assessment_id}/
                sub_criterias/{sub_criteria_id}/scores
                with and json payload
        THEN an score and justification record is created and returned
        :param client:
        """
        assessment_id = seeded_assessment_ids[1]
        sub_criteria_id = seeded_subcriteria[2].id
        endpoint = (
            f"/assessments/{assessment_id}/sub_criterias/"
            f"{sub_criteria_id}/scores"
        )
        payload = {
            "justification": "bad",
            "assessor_user_id": "person_2",
            "score": 1,
        }
        response = client.post(endpoint, json=payload)
        score_justification = response.get_json()

        assert response.status_code == 201
        assert score_justification.get("score") == 1


# TODO FS-1344 reinstate this when we go back to assessment. Currently points
# at data on test which isn't compatible with this test. Should use fixed
# test data
# def test_scores(self, client):
#     expected_response = [
#         {
#             "criteria_id": str(SqliteTestDB.crit_1_uuid),
#             "criteria_name": "strategy",
#             "total_score": 5,
#             "weight": 0.3,
#             "weighted_score": 1.5,
#         },
#         {
#             "criteria_id": str(SqliteTestDB.crit_2_uuid),
#             "criteria_name": "deliverability",
#             "total_score": 6,
#             "weight": 0.4,
#             "weighted_score": 2.4000000000000004,
#         },
#         {
#             "criteria_id": str(SqliteTestDB.crit_3_uuid),
#             "criteria_name": "value_for_money",
#             "total_score": 5,
#             "weight": 0.3,
#             "weighted_score": 1.5,
#         },
#     ]
#     assessment_id = str(SqliteTestDB.assessment_2_uuid)
#     endpoint = f"/assessments/{assessment_id}/scores"
#     response = client.get(endpoint)
#     assert response.json["scores"] == expected_response
