import json
import os

import requests
from app import app
from db.queries.assessment_records.queries import (
    bulk_update_location_jsonb_blob,
)
from db.queries.assessment_records.queries import get_application_jsonb_blob
from db.queries.assessment_records.queries import (
    get_metadata_for_fund_round_id,
)
from fsd_utils.config.commonconfig import CommonConfig

# File locations used by the functions in this script

local_workspace = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

file_raw_forms_data = local_workspace + "/scripts/dev_forms_raw.txt"
file_just_postcodes = local_workspace + "/scripts/postcodes.json"
file_raw_postcode_data = local_workspace + "/scripts/postcode_data_raw.json"
file_locations_result = local_workspace + "/data/locations_dev.json"


"""
1. input?
2. DB query to get all applications
3. for each ->
    3.1. Call get_application_jsonb_blob() from queries.py
    3.2. extract_postcode_from_form()
    3.3. retrieve_data_from_postcodes_io()
    3.4. process_postcode_data()
    3.5. Store into newly created "locations_jsonBlob" field in DB
4. Save data back to DB
"""


def get_application_form(app_json_blob):
    """function return list of all questions from application form"""

    return [
        questions
        for forms in app_json_blob["jsonb_blob"]["forms"]
        for questions in forms["questions"]
    ]


def get_postcode_from_questions(form_questions) -> str:

    for question in form_questions:
        for field in question["fields"]:
            if field["key"] == "yEmHpp":
                answer = field["answer"]
                raw_postcode = answer.split(",")[-1]
                if raw_postcode:
                    postcode = raw_postcode.strip().replace(" ", "").upper()
                    return postcode


def get_all_application_ids() -> list:
    metadata = get_metadata_for_fund_round_id(
        CommonConfig.COF_FUND_ID, CommonConfig.COF_ROUND_2_ID, "", "", ""
    )
    application_ids = [item["application_id"] for item in metadata]
    print(application_ids)
    return application_ids


"""
    Takes the json array of postcodes from previous function, sends it to
    postcodes.io bulk postcode lookup api and then writes the result to the
    specified file
"""


def retrieve_data_from_postcodes_io(postcodes: list):
    result = requests.post(
        url="http://api.postcodes.io/postcodes", data={"postcodes": postcodes}
    )

    return result


def extract_location_data(json_data_item):
    details = json_data_item["result"]
    postcode = json_data_item["query"]
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
    return result


"""
    Takes the result of the previous function, extracts the fields we need
    and writes them to the specified file as a json array with a key of
    postcode. Returns country, constituency, region & constituency
"""


def process_postcode_data():
    postcode_data = []
    with open(file_raw_postcode_data) as f:
        json_data = json.load(f)
        for item in json_data["result"]:
            result = extract_location_data(item)
            postcode_data.append(result)

    with open(file_locations_result, "w") as outfile:
        json.dump(postcode_data, outfile)
    print("Processed postcode data; returned as data/locations_dev.json")


def get_all_location_data(just_postcodes) -> dict:

    raw_location_data = retrieve_data_from_postcodes_io(just_postcodes)

    postcodes_to_location_data = {}
    for postcode_data_item in raw_location_data.json()["result"]:
        postcode = postcode_data_item["query"]
        location_data = extract_location_data(postcode_data_item)
        postcodes_to_location_data[postcode] = location_data[postcode]

    return postcodes_to_location_data


def update_db_with_location_data(
    application_ids_to_postcodes, postcodes_to_location_data
):

    application_ids_to_location_data = [
        {
            "application_id": application_id,
            "location": postcodes_to_location_data[postcode],
        }
        for application_id, postcode in application_ids_to_postcodes.items()
    ]
    bulk_update_location_jsonb_blob(application_ids_to_location_data)


with app.app_context():
    application_ids = get_all_application_ids()
    just_postcodes = []
    application_ids_to_postcodes = {}

    # extract the postcode from each application we have
    for id in application_ids:
        app_json = get_application_jsonb_blob(id)
        questions = get_application_form(app_json)
        postcode = get_postcode_from_questions(questions)
        application_ids_to_postcodes[id] = postcode
        just_postcodes.append(postcode)

    print(just_postcodes)
    print(application_ids_to_postcodes)

    postcodes_to_location_data = get_all_location_data(just_postcodes)

    print(postcodes_to_location_data)
    update_db_with_location_data(
        application_ids_to_postcodes, postcodes_to_location_data
    )


# call this? retrieve_location_data_for_each_application ?

# extract_postcodes_from_forms()

# retrieve_data_from_postcodes_io()

# process_postcode_data()
