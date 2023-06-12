from tests._application_store_json import application_store_json_template
from tests._application_store_json import (
    cofr3w1_application_store_json_template,
)
from tests._application_store_json import (
    nstfr2_application_store_json_template,
)

mappings_application_store_json = {
    "COFR2W2": application_store_json_template,
    "COFR2W3": application_store_json_template,
    "COFR3W1": cofr3w1_application_store_json_template,
    "NSTFR2": nstfr2_application_store_json_template,
    "RANDOM_FUND_ROUND": application_store_json_template,
}

mappings_short_ref = {
    "COFR2W2": "COF-R2W2",
    "COFR2W3": "COF-R2W3",
    "COFR3W1": "COF-R3W1",
    "NSTFR2": "NSTF-R2",
    "RANDOM_FUND_ROUND": "RFR",
}


def get_dynamic_rows(
    number_of_apps_per_round,
    number_of_funds,
    number_of_rounds,
    fund_round_config_dict,
):
    from random import choice, sample
    from string import ascii_uppercase
    from uuid import uuid4

    fund_round_short_name = list(fund_round_config_dict.keys())[0]
    fund_round_config = fund_round_config_dict[fund_round_short_name]
    application_store_json = mappings_application_store_json[
        fund_round_short_name
    ]

    application_short_ref_prefix = mappings_short_ref[fund_round_short_name]

    funds = (
        [fund_round_config["fund_id"]]
        if fund_round_config
        else [uuid4() for _ in range(number_of_funds)]
    )

    verbs = ["Save", "Restore", "Refurbish", "Rebuild", "Remodel"]

    adjects = ["old", "humble", "derelict", "vintage", "loved", "beautiful"]

    places = [
        ("skatepark", "sporting"),
        ("pub", "pub"),
        ("cinema", "cinema"),
        ("community centre", "community-centre"),
        ("gallery", "gallery"),
        ("museum", "museum"),
    ]
    cities = [
        ("Bath", "England"),
        ("Birmingham", "England"),
        ("Bradford", "England"),
        ("Brighton", "England"),
        ("Bristol", "England"),
        ("Cambridge", "England"),
        ("Canterbury", "England"),
        ("Carlisle", "England"),
        ("Chelmsford", "England"),
        ("Chichester", "England"),
        ("Colchester", "England"),
        ("Exeter", "England", "EX44NT"),
        ("Gloucester", "England"),
        ("Hereford", "England"),
        ("Aberdeen", "Scotland", "AB11 6LX"),
        ("Dundee", "Scotland"),
        ("Dunfermline", "Scotland"),
        ("Edinburgh", "Scotland"),
        ("Bangor", "Wales"),
        ("Cardiff", "Wales", "CF10 1EP"),
        ("Newport", "Wales", "NP10 8QQ"),
    ]

    for count, fund_id in enumerate(funds):
        print("fund id:", fund_id)

        rounds = (
            [fund_round_config["round_id"]]
            if fund_round_config
            else [uuid4() for _ in range(number_of_rounds)]
        )

        for round_id in rounds:
            print("round id:", round_id)

            app_ids = [uuid4() for _ in range(number_of_apps_per_round)]

            for app_id in app_ids:
                print("application id:", app_id)
                picked_place = choice(places)
                picked_city = choice(cities)

                project_name = (
                    f"{choice(verbs)} the"
                    f" {choice(adjects)} {picked_place[0]} in {picked_city[0]}"
                )

                short_ref = (
                    application_short_ref_prefix
                    + "-"
                    + "".join(sample(ascii_uppercase, 6))
                )

                print("Seeding db inc location info")
                location_json_blob = {
                    "location_error": "false",
                    "location_county": "test-county",
                    "location_region": picked_city[1],
                    "location_country": picked_city[1],
                    "location_postcode": picked_city[2]
                    if len(picked_city) > 2
                    else "QQ12QQ",
                    "location_constituency": "test-constituency",
                }
                yield application_store_json.substitute(
                    app_id=app_id,
                    project_name=project_name,
                    short_ref=short_ref,
                    round_id=round_id,
                    fund_id=fund_id,
                    asset_type=picked_place[1],
                    **location_json_blob,
                )
