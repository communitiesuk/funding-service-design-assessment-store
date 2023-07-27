import json
import random
from unittest import mock
from uuid import uuid4

import pytest
from api.routes.subcriterias.get_sub_criteria import (
    map_application_with_sub_criteria_themes,
)
from config.mappings.assessment_mapping_fund_round import (
    applicant_info_mapping,
)
from db.models.flags.enums import FlagType
from db.models.flags_v2.assessment_flag import AssessmentFlag
from db.models.flags_v2.flag_update import FlagStatus
from db.models.tag.tags import Tag
from db.queries.flags.queries import create_flag_for_application
from db.queries.flags_v2.queries import (
    create_flag_for_application as create_flag_for_application_v2,
)
from tests._expected_responses import APPLICATION_METADATA_RESPONSE
from tests._expected_responses import ASSESSMENTS_STATS_RESPONSE
from tests.conftest import test_input_data
from tests.test_data.flags import add_flag_update_request_json
from tests.test_data.flags import create_flag_request_json

from ._expected_responses import subcriteria_themes_and_expected_response

COF_FUND_ID = "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4"
COF_ROUND_2_ID = "c603d114-5364-4474-a0c4-c41cbf4d3bbd"
COF_ROUND_2_W3_ID = "5cf439bf-ef6f-431e-92c5-a1d90a4dd32f"
NS_FUND_ID = "13b95669-ed98-4840-8652-d6b7a19964db"
NS_ROUND_2_ID = "fc7aa604-989e-4364-98a7-d1234271435a"


@pytest.mark.apps_to_insert(test_input_data)
def test_get_assessments_stats(client, seed_application_records):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    # Get test applications
    applications = client.get(
        f"/application_overviews/{fund_id}/{round_id}"
    ).json

    # Add a QA_COMPLETED flag for the first application
    # so that one result from the set is flagged as QA_COMPLETED
    create_flag_for_application(
        justification="bob",
        sections_to_flag=["Overview"],
        application_id=applications[0]["application_id"],
        user_id="abc",
        flag_type=FlagType.QA_COMPLETED,
    )

    response_json = client.get(
        f"/assessments/get-stats/{fund_id}/{round_id}"
    ).json

    assert response_json == ASSESSMENTS_STATS_RESPONSE

    # Test number of QA_COMPLETE Applications is correct
    # Add one more QA_COMPLETE flag to another application
    # and also FLAGGED so we can see that the most recent
    # flag does not interfere
    # "qa_completed" should return 2

    create_flag_for_application(
        justification="QA Complete Test 1",
        sections_to_flag=["Overview"],
        application_id=applications[1]["application_id"],
        user_id="abc",
        flag_type=FlagType.QA_COMPLETED,
    )

    create_flag_for_application(
        justification="QA Complete Test 1",
        sections_to_flag=["Overview"],
        application_id=applications[1]["application_id"],
        user_id="abc",
        flag_type=FlagType.FLAGGED,
    )

    response_json = client.get(
        f"/assessments/get-stats/{fund_id}/{round_id}"
    ).json

    assert response_json["qa_completed"] == 2


@pytest.mark.apps_to_insert([test_input_data[0].copy() for x in range(4)])
def test_gets_all_apps_for_fund_round(
    request, client, seed_application_records
):
    """test_gets_all_apps_for_fund_round Tests that the number of rows returned
    by filtering by round on `assessment_records` matches the number of
    applications per round specified by the test data generation process."""

    picked_row = seed_application_records[0]

    apps_per_round = 4

    random_round_id = picked_row["round_id"]
    random_fund_id = picked_row["fund_id"]
    application_id = picked_row["application_id"]

    response_json = client.get(
        f"/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    assert len(response_json) == apps_per_round

    # Check application overview returns flags in order of descending
    create_flag_for_application(
        justification="Test 1",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        flag_type=FlagType.FLAGGED,
    )

    create_flag_for_application(
        justification="Test 2",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        flag_type=FlagType.RESOLVED,
    )

    create_flag_for_application(
        justification="Test 3",
        sections_to_flag=["Overview"],
        application_id=application_id,
        user_id="abc",
        flag_type=FlagType.STOPPED,
    )

    response_with_flag_json = client.get(
        f"/application_overviews/{random_fund_id}/{random_round_id}"
    ).json

    application_to_check = None
    for application in response_with_flag_json:

        if application["application_id"] == application_id:
            application_to_check = application

    # Check that the last flag in the flag array is the latest flag added
    assert application_to_check["flags"][-1]["flag_type"] == "STOPPED"
    assert application_to_check["flags"][-1]["justification"] == "Test 3"


@pytest.mark.parametrize(
    "url, expected_count",
    [
        (
            f"{COF_FUND_ID}/{COF_ROUND_2_ID}?search_term={test_input_data[0]['reference']}&search_in=short_id",
            1,
        ),
        (
            f"{COF_FUND_ID}/{COF_ROUND_2_ID}?search_term=insertion&search_in=project_name",
            2,
        ),
        (f"{COF_FUND_ID}/{COF_ROUND_2_ID}?asset_type=pub", 1),
        (f"{COF_FUND_ID}/{COF_ROUND_2_ID}?status=NOT_STARTED", 3),
        (
            f"{COF_FUND_ID}/{COF_ROUND_2_ID}?search_term={test_input_data[0]['reference']}"
            + "&search_in=short_id&asset_type=BAD",
            0,
        ),
        (
            f"{COF_FUND_ID}/{COF_ROUND_2_ID}?search_term={test_input_data[0]['reference']}",
            3,
        ),
        (
            f"{NS_FUND_ID}/{NS_ROUND_2_ID}?search_term=shelter&search_in=organisation_name",
            1,
        ),
        (
            f"{NS_FUND_ID}/{NS_ROUND_2_ID}?search_term=bad_search&search_in=organisation_name",
            0,
        ),
        (f"{NS_FUND_ID}/{NS_ROUND_2_ID}?funding_type=capital", 1),
        (f"{NS_FUND_ID}/{NS_ROUND_2_ID}?funding_type=revenue", 0),
        (
            f"{NS_FUND_ID}/{NS_ROUND_2_ID}?search_term=shelter&search_in=organisation_name&funding_type=revenue",
            0,
        ),
    ],
)
@pytest.mark.apps_to_insert(test_input_data)
def test_search(url, expected_count, client, seed_application_records):

    response_json = client.get("/application_overviews/" + url).json

    assert len(response_json) == expected_count


@pytest.mark.skip(reason="used for tdd only")
def test_get_application_metadata_for_application_id(client):
    response_json = client.get(
        "/application_overviews/a3ec41db-3eac-4220-90db-c92dea049c00"
    ).json

    assert response_json == APPLICATION_METADATA_RESPONSE


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria(client, seed_application_records):
    """Test to check that sub criteria metadata and ordered themes are returned for
    a COFR2W2 sub criteria"""

    sub_criteria_id = "benefits"
    application_id = seed_application_records[0]["application_id"]
    response_json = client.get(
        f"/sub_criteria_overview/{application_id}/{sub_criteria_id}"
    ).json
    # The order of themes within a sub_criteria is important,
    # ensure it is preserved
    expected_theme_order = ["community_use", "risk_loss_impact"]
    actual_theme_order = []
    for theme in response_json["themes"]:
        actual_theme_order.append(theme["id"])
    assert expected_theme_order == actual_theme_order
    assert "short_id" in response_json
    assert "id" in response_json


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_metadata_for_false_sub_criteria_id(
    client, seed_application_records
):
    """Test to check that sub criteria metadata is
    not retuned for false sub criteria"""

    sub_criteria_id = "does-not-exist"
    application_id = seed_application_records[0]["application_id"]
    response = client.get(
        f"/sub_criteria_overview/{application_id}/{sub_criteria_id}"
    ).json

    assert response["status"] == 404
    assert response["title"] == "Not Found"
    assert response["detail"] == "sub_criteria: 'does-not-exist' not found."


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_theme_answers_field_id(
    request, client, seed_application_records
):
    """Test to check field_id with given application_id and
    theme_id"""

    theme_id = "feasibility"
    application_id = seed_application_records[0]["application_id"]

    response = client.get(f"/sub_criteria_themes/{application_id}/{theme_id}")

    assert response.json[0]["field_id"] == "ieRCkI"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_update_ar_status_to_completed(
    request, client, seed_application_records
):
    """Test checks that the status code returned by the POST request is 204,
    which indicates that the request was successful and
    that the application status was updated to COMPLETED."""

    application_id = seed_application_records[0]["application_id"]
    response = client.post(f"/application/{application_id}/status/complete")

    assert response.status_code == 204


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_add_another_presentation_type(
    request, client, seed_application_records
):
    """Test to check presentation_types for add_another component
    with given application_id and theme_id"""

    theme_id = "funding_requested"
    application_id = seed_application_records[0]["application_id"]

    response = client.get(f"/sub_criteria_themes/{application_id}/{theme_id}")

    assert response.status_code == 200
    assert response.json[0]["presentation_type"] == "grouped_fields"
    assert response.json[1]["presentation_type"] == "heading"
    assert response.json[2]["presentation_type"] == "description"
    assert response.json[3]["presentation_type"] == "amount"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_incorrect_theme_id(request, client, seed_application_records):
    """Test to check incorrect theme_id that is expected
    to return custom error along with the openapi validation
    error."""

    theme_id = "incorrect-theme-id"
    application_id = seed_application_records[0]["application_id"]

    response = client.get(f"/sub_criteria_themes/{application_id}/{theme_id}")

    assert "Incorrect theme id" in response.json["detail"]


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_random_theme_content(seed_application_records):
    """Test the function with random theme id that maps
    the application & subcriteria theme and
    returns subcriteria_theme with an answer from
    application
    """
    application_id = seed_application_records[0]["application_id"]
    theme_id, expected_response = random.choice(
        list(subcriteria_themes_and_expected_response.items())
    )
    result = map_application_with_sub_criteria_themes(
        application_id,
        theme_id,
        COF_FUND_ID,
        COF_ROUND_2_W3_ID,
    )

    assert result[0]["answer"] == expected_response


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_convert_boolean_values(seed_application_records):
    """Test the function that convert boolean values to
    "Yes" and "No".
    Args: application_id, theme_id.
    """

    theme_id = "local-support"
    application_id = seed_application_records[0]["application_id"]

    results = map_application_with_sub_criteria_themes(
        application_id,
        theme_id,
        COF_FUND_ID,
        COF_ROUND_2_W3_ID,
    )

    assert [
        value["answer"] for value in results if value["field_id"] == "KqoaJL"
    ][0] == "No"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_application_json(client, seed_application_records):
    application_id = seed_application_records[0]["application_id"]
    response = client.get(f"/application/{application_id}/json")
    assert 200 == response.status_code

    json_blob = response.json
    assert application_id == json_blob["application_id"]


expected_flag = AssessmentFlag(
    application_id=uuid4(),
    id=uuid4(),
    latest_status=FlagStatus.STOPPED,
    latest_allocation="TEAM_2",
    sections_to_flag=[],
    updates=[],
)


def test_get_flags_v2(client, mocker):
    mocker.patch(
        "api.routes.assessment_routes.get_flags_for_application",
        return_value=[expected_flag],
    )
    response = client.get("/flags_v2/app_id")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == str(expected_flag.id)


@pytest.mark.apps_to_insert([test_input_data[0].copy() for x in range(4)])
def test_get_team_flag_stats(client, seed_application_records):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    # Get test applications
    applications = client.get(
        f"/application_overviews_flags_v2/{fund_id}/{round_id}"
    ).json

    # Add a RAISED flag for the first application
    # so that one result from the set is flagged as RAISED
    # and only one team exists with a flag allocated
    create_flag_for_application_v2(
        justification="bob",
        sections_to_flag=["Overview"],
        application_id=applications[0]["application_id"],
        user_id="abc",
        status="RAISED",
        allocation="ASSESSOR",
    )

    response = client.get(
        f"/assessments/get-team-flag-stats/{fund_id}/{round_id}"
    )

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["team_name"] == "ASSESSOR"
    assert response.json[0]["raised"] == 1

    # Add a RAISED flag for second application
    # still only one team exists with a flag allocated
    # response should still have only one row for one team
    # 2 raised
    create_flag_for_application_v2(
        justification="bob",
        sections_to_flag=["Overview"],
        application_id=applications[1]["application_id"],
        user_id="abc",
        status="RAISED",
        allocation="ASSESSOR",
    )

    # Add a RAISED flag for first application
    # for a second team response have 2 rows for the two teams
    create_flag_for_application_v2(
        justification="bob",
        sections_to_flag=["Overview"],
        application_id=applications[1]["application_id"],
        user_id="abc",
        status="RAISED",
        allocation="LEAD_ASSESSOR",
    )

    response = client.get(
        f"/assessments/get-team-flag-stats/{fund_id}/{round_id}"
    )

    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["team_name"] == "ASSESSOR"
    assert response.json[0]["raised"] == 2
    assert response.json[1]["team_name"] == "LEAD_ASSESSOR"
    assert response.json[1]["raised"] == 1


def test_create_flag_v2(client):
    request_body = {
        **create_flag_request_json,
        "application_id": str(uuid4()),
    }
    with mock.patch(
        "api.routes.assessment_routes.create_flag_for_application",
        return_value=expected_flag,
    ) as create_mock:
        response = client.post(
            "/flags_v2/",
            data=json.dumps(request_body),
            content_type="application/json",
        )
        assert response.status_code == 200
        create_mock.assert_called_with(**request_body)
        assert response.json["id"] == str(expected_flag.id)


def test_update_flag_v2(client):
    request_body = {
        **add_flag_update_request_json,
        "assessment_flag_id": str(uuid4()),
    }
    with mock.patch(
        "api.routes.assessment_routes.add_update_to_assessment_flag",
        return_value=expected_flag,
    ) as update_mock:
        response = client.put(
            "/flags_v2/",
            data=json.dumps(request_body),
            content_type="application/json",
        )
        assert response.status_code == 200
        update_mock.assert_called_once_with(**request_body)
        assert response.json["id"] == str(expected_flag.id)


def test_get_tag(client, mocker):
    tag_id = uuid4()
    mock_tag = Tag(
        id=tag_id,
        value="tag value 1",
        creator_user_id="test-user",
        active=True,
        fund_id=uuid4(),
        round_id=uuid4(),
        type_id=uuid4(),
    )
    with mocker.patch(
        "api.routes.tag_routes.get_tag_by_id", return_value=mock_tag
    ):
        response = client.get("/funds/test-fund/rounds/round-id/tags/tag-id")
        assert response.status_code == 200
        assert response.json
        assert response.json["id"] == str(tag_id)


def test_get_tag_none_exists(client, mocker):
    with mocker.patch(
        "api.routes.tag_routes.get_tag_by_id", return_value=None
    ):
        response = client.get("/funds/test-fund/rounds/round-id/tags/tag-id")
        assert response.status_code == 404


@pytest.mark.apps_to_insert([test_input_data[0].copy() for x in range(4)])
@pytest.mark.unique_fund_round(True)
def test_get_application_fields_exportt(
    client, seed_application_records, monkeypatch
):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    monkeypatch.setitem(
        applicant_info_mapping,
        f"{fund_id}",
        {"aHIGbK", "aAeszH", "ozgwXq", "KAgrBz"},
    )

    result = client.get(
        f"/application_fields_export/{fund_id}/{round_id}"
    ).json  # noqa

    assert len(result) == 4
    assert result[0]["Charity number "] == "Test"
    assert (
        result[0]["Do you need to do any further feasibility work?"] is False
    )
    assert result[0]["Project name"] == "Save the humble pub in Bangor"
    assert (
        result[0]["Risks to your project (document upload)"] == "sample1.doc"
    )
