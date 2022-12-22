import json

import requests

# File locations used by the functions in this script

local_workspace = "/path/to/workspace/"
file_raw_forms_data = (
    local_workspace
    + "funding-service-design-assessment-store/scripts/dev_forms_raw.txt"
)
file_just_postcodes = (
    local_workspace
    + "funding-service-design-assessment-store/scripts/postcodes.json"
)
file_raw_postcode_data = (
    local_workspace
    + "funding-service-design-assessment-store/scripts/postcode_data_raw.json"
)
file_locations_result = (
    local_workspace
    + "funding-service-design-assessment-store/data/locations_dev.json"
)


"""
    Goes through form jsons to find the address of asset field, extracts the
    postcode and writes the resulting json array of postcodes to the specified
    file
"""


def extract_postcodes_from_forms():
    address_key = "yEmHpp"
    with open(file_raw_forms_data) as f:
        lines = f.readlines()
        results = []
        for line in lines:
            json_str = '{"form":' + line + "}"
            json_line = json.loads(json_str)
            if len(json_line["form"]) > 0:
                for question in json_line["form"]:
                    for field in question["fields"]:
                        if field["key"] == address_key:
                            answer = field["answer"]
                            raw_postcode = answer.split(",")[-1]
                            if raw_postcode:
                                postcode = (
                                    raw_postcode.strip()
                                    .replace(" ", "")
                                    .upper()
                                )
                                results.append(postcode)

        print(f"found {len(results)} postcodes")
        with open(file_just_postcodes.json, "w") as f:
            json_out = {"postcodes": results}
            json.dump(json_out, f)


"""
    Takes the json array of postcodes from previous function, sends it to
    postcodes.io bulk postcode lookup api and then writes the result to the
    specified file
"""


def retrieve_data_from_postcodes_io():
    with open(file_just_postcodes) as f:
        json_in = json.load(f)
        result = requests.post(
            url="http://api.postcodes.io/postcodes", data=json_in
        )

    with open(file_raw_postcode_data, "w") as f:
        json.dump(result.json(), f)


"""
    Takes the result of the previous function, extracts the fields we need
    and writes them to the specified file as a json array with a key of
    postcode.
"""


def process_postcode_data():

    postcode_data = []
    with open(file_raw_postcode_data) as f:
        json_data = json.load(f)
        for item in json_data["result"]:
            details = item["result"]
            postcode = item["query"]
            if details:
                region = (
                    details["region"]
                    if details["region"]
                    else details["european_electoral_region"]
                )
                county = (
                    details["admin_county"]
                    if details["admin_county"]
                    else details["admin_district"]
                )
                result = {
                    postcode: {
                        "error": False,
                        "country": details["country"],
                        "constituency": details["parliamentary_constituency"],
                        "region": region,
                        "county": county,
                    }
                }
            else:
                result = {postcode: {"error": True}}
            postcode_data.append(result)
        print(len(postcode_data))

    with open(file_locations_result, "w") as f:
        json.dump(postcode_data, f)


# extract_postcodes_from_forms()

# retrieve_data_from_postcodes_io()

# process_postcode_data()
