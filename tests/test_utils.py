from unittest import mock

from api.routes.scores_justifications import utils

STRATEGIC_CASE_ID = "123"


def mock_get_round(*args, **kwargs):
    return {
        "assessment_criteria_weighting": [
            {"id": STRATEGIC_CASE_ID, "name": "Strategic case", "value": 0.8},
        ]
    }


class Test_Utils:
    def test_calc_weights_by_id(self):
        with mock.patch(
            "api.routes.scores_justifications.utils.get_round_json",
            side_effect=mock_get_round,
        ):
            result = utils.calc_weighted_scores_for_criteria(
                fund_id="fund_1",
                round_id="round_1",
                crit_id=STRATEGIC_CASE_ID,
                crit_name="Strategic Case",
                list_of_scores=[4, 6],
                query_by_name=False,
            )
        assert 10 == result["total_score"], "Wrong total score"
        assert 8 == result["weighted_score"], "Wrong weighted score"
        assert 0.8 == result["weight"]

    def test_calc_weights_by_name(self):
        with mock.patch(
            "api.routes.scores_justifications.utils.get_round_json",
            side_effect=mock_get_round,
        ):
            result = utils.calc_weighted_scores_for_criteria(
                fund_id="fund_1",
                round_id="round_1",
                crit_id=STRATEGIC_CASE_ID,
                crit_name="Strategic case",
                list_of_scores=[12, 8],
                query_by_name=True,
            )
        assert 20 == result["total_score"], "Wrong total score"
        assert 16 == result["weighted_score"], "Wrong weighted score"
        assert 0.8 == result["weight"]
