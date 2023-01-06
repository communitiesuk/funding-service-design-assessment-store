from db.queries.assessment_records.queries import get_application_jsonb_blob

import json
import os

import requests

# File locations used by the functions in this script

local_workspace = (os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

file_raw_forms_data = (
        local_workspace + "/scripts/dev_forms_raw.txt"
)
file_just_postcodes = (
        local_workspace + "/scripts/postcodes.json"
)
file_raw_postcode_data = (
        local_workspace + "/scripts/postcode_data_raw.json"
)
file_locations_result = (
        local_workspace + "/data/locations_dev.json"
)

"""
    Goes through form jsons to find the address of asset field, extracts the
    postcode and writes the resulting json array of postcodes to the specified
    file
"""

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

def extractPostCodeData():

    application_id = "test-application-id"
    application_json_blob = get_application_jsonb_blob(application_id)
    questions = get_application_form(application_json_blob)

    locationResults = []
    for question in questions:
        for field in question["fields"]:
            if field["key"] == "yEmHpp":
                answer = field["answer"]
                raw_postcode = answer.split(",")[-1]
                if raw_postcode:
                    postcode = (
                        raw_postcode.strip()
                        .replace(" ", "")
                        .upper()
                    )
                    locationResults.append(postcode)
    print(f"Found {len(locationResults)} Test")


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

        print(f"Found {len(results)} Postcodes in provided raw data")
        # will consider iterating through and removing duplicates
        with open('file_just_postcodes', 'w') as outfile:
            json_out = {"postcodes": results}
            json.dump(json_out, outfile)
        print("Extracted list of postcodes from raw data; returned as scripts/postcodes.json")


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

    with open('file_raw_postcode_data', 'w') as outfile:
        json.dump(result.json(), outfile)
    print("Retrieved all postcode data; returned as scripts/file_just_postcodes.json")


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

    with open(file_locations_result, "w") as outfile:
        json.dump(postcode_data, outfile)
    print("Processed postcode data; returned as data/locations_dev.json")


extractPostCodeData()
# call this? retrieve_location_data_for_each_application ?

#extract_postcodes_from_forms()

#retrieve_data_from_postcodes_io()

#process_postcode_data()
