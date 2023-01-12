import csv

import requests
from db.queries.assessment_records.queries import (
    bulk_update_location_jsonb_blob,
)
from db.queries.assessment_records.queries import (
    get_metadata_for_fund_round_id,
)


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


def get_all_application_ids_for_fund_round(fund_id, round_id) -> list:
    metadata = get_metadata_for_fund_round_id(fund_id, round_id, "", "", "")
    application_ids = [item["application_id"] for item in metadata]
    print(application_ids)
    return application_ids


"""
    Takes a list of postcodes andsends it to
    postcodes.io bulk postcode lookup api and then writes the result to the
    specified file"""


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
                "postcode": postcode,
                "country": details["country"],
                "constituency": details["parliamentary_constituency"],
                "region": region,
                "county": county,
            }
        }
    else:
        result = {postcode: {"error": True}}
    return result


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


def write_locations_to_csv(
    application_ids_to_postcodes, postcodes_to_location_data, file_path
):

    with open(file_path, "w", newline="") as csvfile:
        fieldnames = [
            "application_id",
            "postcode",
            "error",
            "county",
            "country",
            "region",
            "constituency",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k, v in application_ids_to_postcodes.items():
            writer.writerow(
                {"application_id": k, **postcodes_to_location_data[v]}
            )
