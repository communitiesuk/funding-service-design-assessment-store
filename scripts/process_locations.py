import json

import requests


def extract_postcodes_from_forms():
    raw_path = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/"
        + "funding-service-design-assessment-store/scripts/dev_forms_raw.txt"
    )
    address_key = "yEmHpp"
    with open(raw_path) as f:
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
        out_file = "/Users/sarahsloan/dev/CommunitiesUkWorkspace/"
        +"funding-service-design-assessment-store/scripts/postcodes.json"
        with open(out_file, "w") as f:
            json_out = {"postcodes": results}
            json.dump(json_out, f)


# extract_postcodes_from_forms()


def retrieve_data_from_postcodes_io():
    in_file = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/"
        + "funding-service-design-assessment-store/scripts/postcodes.json"
    )
    postcode_data_file = "/Users/sarahsloan/dev/CommunitiesUkWorkspace/"
    +"funding-service-design-assessment-store/scripts/postcode_data_raw.json"
    with open(in_file) as f:
        json_in = json.load(f)
        result = requests.post(
            url="http://api.postcodes.io/postcodes", data=json_in
        )

    with open(postcode_data_file, "w") as f:
        json.dump(result.json(), f)


# retrieve_data_from_postcodes_io()


def process_postcode_data():
    postcode_data_file = "/Users/sarahsloan/dev/CommunitiesUkWorkspace/"
    +"funding-service-design-assessment-store/scripts/postcode_data_raw.json"

    postcode_data = []
    with open(postcode_data_file) as f:
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

    out_file = (
        "/Users/sarahsloan/dev/CommunitiesUkWorkspace/"
        + "funding-service-design-assessment-store/data/locations_dev.json"
    )
    with open(out_file, "w") as f:
        json.dump(postcode_data, f)


process_postcode_data()
