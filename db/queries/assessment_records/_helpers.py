import jsonpath_rw_ext


def derive_application_values(application_json):
    # TODO: implement mapping function to match
    #  fund+round fields to derived values
    derived_values = {}
    application_id = application_json["id"]
    print(f"deriving values for application id: {application_id}.")
    try:
        asset_type = (
            jsonpath_rw_ext.parse(
                '$.forms[*].questions[*].fields[?(@.key == "yaQoxU")]'
            )
            .find(application_json)[0]
            .value["answer"]
        )
    except Exception:
        print(
            f"Could not extract asset_type from application: {application_id}."
        )
        asset_type = "Not asset type specified."
    try:
        funding_one = (
            jsonpath_rw_ext.parse(
                '$.forms[*].questions[*].fields[?(@.key =="JzWvhj")]'
            )
            .find(application_json)[0]
            .value["answer"]
        ) or 0
    except Exception:
        print(
            f"Could not extract funding_value_one from application: {application_id}."
        )
        funding_one = 0
    try:
        funding_two = (
            jsonpath_rw_ext.parse(
                '$.forms[*].questions[*].fields[?(@.key == "jLIgoi")]'
            )
            .find(application_json)[0]
            .value["answer"]
        ) or 0
    except Exception:
        print(
            f"Could not extract funding_value_two from application: {application_id}."
        )
        funding_two = 0
    derived_values["application_id"] = application_id
    derived_values["project_name"] = application_json["project_name"]
    derived_values["short_id"] = application_json["reference"]
    derived_values["fund_id"] = application_json["fund_id"]
    derived_values["round_id"] = application_json["round_id"]
    derived_values["funding_amount_requested"] = (
        int(float(funding_one))
        + int(float(funding_two))
    )
    derived_values["asset_type"] = asset_type

    derived_values["location_json_blob"] = application_json["location_json_blob"]

    if derived_values["location_json_blob"].get('error') is 'true':
        derived_values["county"] = "Not Available."
        derived_values["region"] = "Not Available."
        derived_values["country"] = "Not Available."
        derived_values["constituency"] = "Not Available."

    return derived_values