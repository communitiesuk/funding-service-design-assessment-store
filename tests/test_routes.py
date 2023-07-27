import cProfile
import json
import random
import string
import timeit
from unittest import mock
from uuid import uuid4

import pytest
from api.routes.subcriterias.get_sub_criteria import (
    map_application_with_sub_criteria_themes,
)
from config.mappings.assessment_mapping_fund_round import (
    applicant_info_mapping,
)
from db import db
from db.models.assessment_record import AssessmentRecord
from db.models.flags.enums import FlagType
from db.models.flags_v2.assessment_flag import AssessmentFlag
from db.models.flags_v2.flag_update import FlagStatus
from db.queries.flags.queries import create_flag_for_application
from db.queries.flags_v2.queries import (
    create_flag_for_application as create_flag_for_application_v2,
)
from sqlalchemy import and_
from sqlalchemy import bindparam
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import text
from sqlalchemy import update
from sqlalchemy.orm import aliased
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


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for i in range(length))


def test_generate_json(client):
    modified_json_list = []
    num_objects = 10

    for _ in range(num_objects):
        # Generate a new JSON object
        modified_json = {
            "account_id": generate_random_string(8),
            "date_submitted": "2023-07-25T12:00:00.000000",
            "forms": [],
            "fund_id": generate_random_string(8),
            "id": generate_random_string(8),
            "last_edited": "2023-07-25T12:00:00.000000",
            "project_name": generate_random_string(20),
            "reference": generate_random_string(10),
            "round_id": generate_random_string(8),
            "round_name": generate_random_string(12),
            "started_at": "2023-07-25T12:00:00.000000",
        }

        # Append the modified JSON object to the list
        modified_json_list.append(modified_json)

    for i, modified_json in enumerate(modified_json_list, 1):
        print(f"Modified JSON Object {i}:")
        print(modified_json)
        print("-" * 40)


@pytest.mark.apps_to_insert([test_input_data[0].copy() for x in range(4)])
@pytest.mark.unique_fund_round(True)
def test_get_application_export(client, seed_application_records, monkeypatch):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    monkeypatch.setitem(
        applicant_info_mapping,
        f"{fund_id}",
        {"aHIGbK", "aAeszH", "ozgwXq", "KAgrBz"},
    )

    result = my_code(fund_id, round_id)

    assert len(result) == 4


data_set1 = [test_input_data[0].copy() for _ in range(4)]
data_set2 = [test_input_data[1].copy() for _ in range(500)]
data_set3 = [test_input_data[2].copy() for _ in range(500)]
data_set4 = [test_input_data[3].copy() for _ in range(500)]
data_set5 = [test_input_data[4].copy() for _ in range(500)]
data_set6 = [test_input_data[5].copy() for _ in range(500)]
data_set7 = [test_input_data[6].copy() for _ in range(500)]
data_set8 = [test_input_data[7].copy() for _ in range(500)]
data_set9 = [test_input_data[8].copy() for _ in range(500)]
data_set10 = [test_input_data[9].copy() for _ in range(500)]
data_set11 = [test_input_data[10].copy() for _ in range(500)]
combined_test_data = (
    data_set1
    + data_set2
    + data_set3
    + data_set4
    + data_set5
    + data_set6
    + data_set7
    + data_set8
    + data_set9
    + data_set10
    + data_set11
)


@pytest.mark.apps_to_insert(data_set1)
def testthis_get_application_export_500(
    client, seed_application_records, monkeypatch
):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    monkeypatch.setitem(
        applicant_info_mapping,
        "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        {"ieRCkI", "aAeszH", "ozgwXq", "CDwTrG"},
    )

    repeat_count = 5  # Number of repetitions for more accurate results
    execution_times = timeit.repeat(
        stmt=lambda: my_code(fund_id=fund_id, round_id=round_id),
        number=1,
        repeat=repeat_count,
    )

    for i, time in enumerate(execution_times, 1):
        print(f"Execution time {i}: {time} seconds")


data_set1 = [test_input_data[0].copy() for _ in range(500)]
data_set2 = [test_input_data[1].copy() for _ in range(500)]
data_set3 = [test_input_data[2].copy() for _ in range(500)]
data_set4 = [test_input_data[3].copy() for _ in range(500)]
data_set5 = [test_input_data[4].copy() for _ in range(500)]
data_set6 = [test_input_data[5].copy() for _ in range(500)]
data_set7 = [test_input_data[6].copy() for _ in range(500)]
data_set8 = [test_input_data[7].copy() for _ in range(500)]
data_set9 = [test_input_data[8].copy() for _ in range(500)]
data_set10 = [test_input_data[9].copy() for _ in range(500)]
data_set11 = [test_input_data[10].copy() for _ in range(500)]
combined_test_data = (
    data_set1
    + data_set2
    + data_set3
    + data_set4
    + data_set5
    + data_set6
    + data_set7
    + data_set8
    + data_set9
    + data_set10
    + data_set11
)


@pytest.mark.apps_to_insert(combined_test_data)
def test_thisget_application_export_500_large_data(
    client, seed_application_records, monkeypatch
):
    fund_id = seed_application_records[0]["fund_id"]
    round_id = seed_application_records[0]["round_id"]

    monkeypatch.setitem(
        applicant_info_mapping,
        "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        {
            "ieRCkI",
            "aAeszH",
            "ozgwXq",
            "CDwTrG",
            "kxgWTy",
            "GNhrIs",
            "qsZLjZ",
            "CvVZJv",
            "KqoaJL",
            "HvxXPI",
            "CBIWnt",
            "vKnMPG",
            "rFXeZo",
            "gScdbf",
            "KAgrBz",
            "wudRxx",
            "TlGjXb",
            "GCjCse",
            "yEmHpp",
            "MGRlEi",
            "WWWWxy",
            "YdtlQZ",
            "iBCGxY",
            "emVGxS",
            "btTtIb",
            "SkocDi",
            "CNeeiC",
            "BBlCko",
            "lajFtB",
            "aHIGbK",
            "DwfHtk",
            "ZQolYb",
            "zsoLdf",
            "FhbaEy",
            "FcdKlB",
            "BzxgDA",
            "hnLurH",
            "ZBjDTn",
            "lRfhGB",
            "yaQoxU",
            "VWkLlk",
            "IRfSZp",
            "FtDJfK",
            "gkulUE",
            "nvMmGE",
            "ghzLRv",
            "Wyesgy",
            "hvzzWB",
            "VwxiGn",
            "UDTxqC",
            "HJBgvw",
            "JCACTy",
            "NZKHOp",
            "JzWvhj",
            "jLIgoi",
            "NWTKzQ",
            "DIZZOC",
            "RvbwSX",
            "fnIdkJ",
            "gDTsgG",
            "kYjJFy",
            "UbjYqE",
            "SrtVAs",
            "YbfbSC",
            "KuhSWw",
            "bkJsiO",
            "WDDkVB",
            "oaIntA",
            "multiInputField-2",
            "JnvsPq",
            "yMCivI",
            "NUZOvS",
            "oOPUXI",
            "NKOmNL",
            "LlvhYl",
            "wJrJWY",
            "COiwQr",
            "bRPzWU",
        },
    )

    repeat_count = 5  # Number of repetitions for more accurate results
    execution_times = timeit.repeat(
        stmt=lambda: my_code(fund_id=fund_id, round_id=round_id),
        number=1,
        repeat=repeat_count,
    )

    for i, time in enumerate(execution_times, 1):
        print(f"Execution time {i}: {time} seconds")


def my_code(fund_id: str, round_id: str):

    assement_alias = aliased(AssessmentRecord)
    list_of_fields = applicant_info_mapping[fund_id]
    rows_list = []

    subquery = db.session.query(assement_alias.application_id)

    # for field_key in list_of_fields:
    #     title_expression = func.jsonb_path_query(
    #         assement_alias.jsonb_blob,
    #         text(f'\'$.forms[*].questions[*].fields[*] ? (@.key == "{field_key}").title\'')
    #     ).label(f'title_{field_key}')

    #     answer_expression = func.jsonb_path_query(
    #         assement_alias.jsonb_blob,
    #         text(f'\'$.forms[*].questions[*].fields[*] ? (@.key == "{field_key}").answer\'')
    #     ).label(f'answer_{field_key}')

    #     subquery = subquery.add_columns(title_expression, answer_expression)

    # subquery = subquery.filter(assement_alias.fund_id == fund_id)
    # subquery = subquery.filter(assement_alias.round_id == round_id)

    # results = subquery.all()

    #  statement = (
    #     select(AssessmentRecord)
    #     .where(
    #         AssessmentRecord.fund_id == fund_id,
    #         AssessmentRecord.round_id == round_id,
    #     )
    # )

    # assessment_metadatas = db.session.scalars(statement).all()

    columns = []

    # Build the columns dynamically for each field_key in list_of_fields
    for field_key in list_of_fields:
        title_expression = func.jsonb_path_query(
            assement_alias.jsonb_blob,
            text(
                f"'$.forms[*].questions[*].fields[*] ? (@.key == \"{field_key}\").title'"
            ),
        ).label(f"title_{field_key}")

        answer_expression = func.jsonb_path_query(
            assement_alias.jsonb_blob,
            text(
                f"'$.forms[*].questions[*].fields[*] ? (@.key == \"{field_key}\").answer'"
            ),
        ).label(f"answer_{field_key}")

        columns.extend([title_expression, answer_expression])

    # Build the main query with the new columns
    statement = select(assement_alias.application_id, *columns).where(
        assement_alias.fund_id == fund_id,
        assement_alias.round_id == round_id,
    )
    # Execute the combined query with a single database call
    result_set = db.session.execute(statement)

    # Fetch all the rows as tuples
    assessment_metadatas = result_set.fetchall()

    # for row in subquery:
    #     app_id = row.application_id
    #     title_key = f'title_{field_key}'
    #     answer_key = f'answer_{field_key}'

    #     # Check if there is an existing row for the AppId
    #     existing_row = next((r for r in rows_list if r["AppId"] == app_id),
    #                         None)
    #     if existing_row is None:
    #         new_row = {"AppId": app_id}
    #         new_row[row[title_key]] = row[answer_key]
    #         rows_list.append(new_row)
    #     else:
    #         existing_row[row[title_key]] = row[answer_key]

    return subquery
