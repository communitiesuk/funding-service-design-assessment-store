import json

from scripts.process_locations import extract_location_data
from scripts.process_locations import get_application_form
from scripts.process_locations import get_postcode_from_questions


def test_get_application_form():

    single_application_json = (
        "tests_no_db/test_data/single_application_jsonb_blob.json"
    )

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)

    result = get_application_form(loaded_test_json)
    assert 45 == len(result), "unexpected number of questions"


def test_get_postcode_from_questions():
    expected = "QQ127QQ"

    test_json_file = (
        "tests_no_db/test_data/questions_from_single_application.json"
    )

    with open(test_json_file, "r") as f:
        loaded_test_json = json.load(f)

    result = get_postcode_from_questions(loaded_test_json)
    assert expected == result, "wrong postcode returned"


def test_extract_location_data_success():
    postcode = "PL13RE"

    test_json_file = "tests_no_db/test_data/postcodes_io_response.json"

    with open(test_json_file, "r") as f:
        loaded_test_json = json.load(f)

    item_under_test = loaded_test_json["result"][1]
    assert postcode == item_under_test["query"]

    result = extract_location_data(item_under_test)
    assert result[postcode]
    assert result[postcode]["error"] is False
    assert result[postcode]["country"] == "England"
    assert result[postcode]["constituency"] == "Plymouth, Sutton and Devonport"
    assert result[postcode]["region"] == "South West"
    assert result[postcode]["county"] == "Plymouth"


def test_extract_location_data_error():
    postcode = "QQ127QQ"

    test_json_file = "tests_no_db/test_data/postcodes_io_response.json"

    with open(test_json_file, "r") as f:
        loaded_test_json = json.load(f)

    item_under_test = loaded_test_json["result"][3]
    assert postcode == item_under_test["query"]

    result = extract_location_data(item_under_test)
    assert result[postcode]
    assert result[postcode]["error"] is True
