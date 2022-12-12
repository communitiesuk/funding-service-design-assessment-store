import pytest
import random

from db.models.assessment_record.assessment_records import AssessmentRecord
from tests._expected_responses import APPLICATION_METADATA_RESPONSE
from tests._helpers import get_random_row
from tests._helpers import get_rows_by_filters
from api.routes.subcriterias.get_sub_criteria import SubCriteriaThemes
from ._expected_responses import subcriteria_themes_and_expected_response



def test_gets_all_apps_for_fund_round(request, client):
    """test_gets_all_apps_for_fund_round Tests that the number of rows returned
    by filtering by round on `assessment_records` matches the number of
    applications per round specified by the test data generation process."""

    picked_row = get_random_row(AssessmentRecord)

    current_run_is_random = request.config.getoption("randomdata")

    if current_run_is_random:
        apps_per_round = request.config.getoption("apps_per_round")
    else:
        # If you regenerate the deterministic test data you will have to change
        # this to the value you used.
        apps_per_round = 100

    random_round_id = picked_row.round_id

    random_fund_id = picked_row.fund_id

    response_json = client.get(
        f"/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    assert len(response_json) == apps_per_round


def test_search(client):

    searchs = [
        {
            "url": "{row.fund_id}/{row.round_id}?search_term={row.short_id}",
            "filter": lambda row: AssessmentRecord.short_id == row.short_id,
        }, 
        {
            "url": "{row.fund_id}/{row.round_id}"
            "?search_term={row.project_name}",
            "filter": lambda row: AssessmentRecord.project_name
            == row.project_name,
        },
        {
            "url": "{row.fund_id}/{row.round_id}?asset_type={row.asset_type}",
            "filter": lambda row: AssessmentRecord.asset_type
            == row.asset_type,
        },
        {
            "url": "{row.fund_id}/{row.round_id}"
            "?status={row.workflow_status.name}",
            "filter": lambda row: AssessmentRecord.workflow_status
            == row.workflow_status.name,
        },
    ]

    for search in searchs:

        picked_row = get_random_row(AssessmentRecord)

        filters = [search["filter"](picked_row)]

        rows = get_rows_by_filters(
            picked_row.fund_id, picked_row.round_id, filters
        )

        response_json = client.get(
            "/application_overviews/" + search["url"].format(row=picked_row)
        ).json

        assert len(response_json) == len(rows)


def test_get_application_metadata_for_application_id(client):
    response_json = client.get(
        f"/application_overviews/a3ec41db-3eac-4220-90db-c92dea049c00"
    ).json

    assert response_json == APPLICATION_METADATA_RESPONSE


@pytest.mark.parametrize("sub_criteria_response_key", ["id", "name", "score_submitted","themes"])
def test_get_sub_criteria(request, client, sub_criteria_response_key):
    """Test to check that sub criteria metadata and ordered themes are returned for
    a COFR2W2 sub criteria"""

    sub_criteria_id = "benefits"
    response_json = client.get(
        f"/sub_criteria_overview/{sub_criteria_id}"
    ).json
    # The order of themes within a sub_criteria is important, ensure it is preserved
    expected_theme_order = ["community_use", "risk_loss_impact"]
    actual_theme_order = []
    for theme in response_json["themes"]:
        actual_theme_order.append(theme["id"])
    assert expected_theme_order == actual_theme_order
    assert sub_criteria_response_key in response_json


def test_get_false_sub_criteria(request, client):
    """Test to check that sub criteria data is not retuned for false sub criteria"""

    sub_criteria_id = "does-not-exist"
    response = client.get(
        f"/sub_criteria_overview/{sub_criteria_id}"
    )


    assert response.json["status"] == 404
    assert response.json["title"] == "Not Found"
    assert response.json["detail"] == "sub_criteria: 'does-not-exist' not found."


def test_get_sub_criteria_theme_answers_field_id(request, client):
    """ Test to check field_id with given application_id and 
    theme_id"""
    
    theme_id = "feasibility"
    application_id = "a3ec41db-3eac-4220-90db-c92dea049c00"
    
    response = client.get(
        f"/sub_criteria_themes/{application_id}/{theme_id}"
    )

    assert response.json[0]['field_id'] == "ieRCkI"
    
def test_add_another_presentation_type(request, client):
    """ Test to check presentation_types for add_another component 
    with given application_id and theme_id"""
    
    theme_id = "funding_requested"
    application_id = "a3ec41db-3eac-4220-90db-c92dea049c00"
    
    response = client.get(
        f"/sub_criteria_themes/{application_id}/{theme_id}"
    )
    assert response.status_code == 200
    assert response.json[0]['presentation_type'] == "grouped_fields"
    assert response.json[1]['presentation_type'] == "heading"
    assert response.json[2]['presentation_type'] == "description"
    assert response.json[3]['presentation_type'] == "amount"
    

theme, expected_response = random.choice(list(subcriteria_themes_and_expected_response.items()))
@pytest.mark.parametrize("app_id, theme_id, expected_response",[
                            ("a3ec41db-3eac-4220-90db-c92dea049c00", theme, expected_response),])
def test_random_theme_content(app_id, theme_id, expected_response):
    """ Test the function with random theme that maps
    the application & subcriteria theme and
    returns subcriteria_theme with an answer from
    application
    """

    result = SubCriteriaThemes.map_application_with_sub_criteria_themes(
            app_id,theme_id )
    assert result [0]['answer'] == expected_response
