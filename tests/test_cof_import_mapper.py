import json

from db.queries.assessment_records._helpers import derive_values_from_json


def test_derive_cof_values():
    single_app = "tests/test_data/single_application.json"

    with open(single_app, "r") as f:
        loaded_json = json.load(f)
    derived_fields = derive_values_from_json(loaded_json, "COF")
    # should this assertion not be the other way around?
    assert "TEST-REF" == derived_fields["short_id"], "Wrong short id"
