import json

from db.queries.assessment_records._helpers import derive_application_values


def test_derive_cof_values_no_location():
    single_application_json = (
        "tests_no_db/test_data/single_application_no_location.json"
    )

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"], "Wrong Short ID"
    assert (
        "funding-service-design" == derived_fields["fund_id"]
    ), "Wrong Fund ID"
    assert "summer" == derived_fields["round_id"], "Wrong Round ID"
    assert (
        "test-application-id" == derived_fields["application_id"]
    ), "Wrong Application ID"
    assert (
        "Project name" == derived_fields["project_name"]
    ), "Wrong Project Name"
    assert (
        "community-centre" == derived_fields["asset_type"]
    ), "Wrong Asset Type"

    assert (
        derived_fields["location_json_blob"]["error"] is True
    ), "wrong error value"
    assert (
        "Not Available" == derived_fields["location_json_blob"]["county"]
    ), "wrong county value"


def test_derive_cof_values_location_present_no_error():
    single_application_json = (
        "tests_no_db/test_data/single_application_no_location.json"
    )

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
    loaded_test_json["location_json_blob"] = {
        "error": False,
        "county": "Cornwall",
        "region": "region",
        "country": "country",
        "constituency": "constituency",
        "postcode": "postcode",
    }
    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"], "Wrong Short ID"

    assert (
        derived_fields["location_json_blob"]["error"] is False
    ), "wrong error value"
    assert (
        "Cornwall" == derived_fields["location_json_blob"]["county"]
    ), "wrong county value"


def test_derive_cof_values_location_present_with_error():
    single_application_json = (
        "tests_no_db/test_data/single_application_no_location.json"
    )

    with open(single_application_json, "r") as f:
        loaded_test_json = json.load(f)
    loaded_test_json["location_json_blob"] = {"error": True, "county": "error"}
    derived_fields = derive_application_values(loaded_test_json)
    assert "TEST-REF" == derived_fields["short_id"], "Wrong Short ID"

    assert (
        derived_fields["location_json_blob"]["error"] is True
    ), "wrong error value"
    assert (
        "Not Available" == derived_fields["location_json_blob"]["county"]
    ), "wrong county value"
