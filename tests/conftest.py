import json
from uuid import uuid4

import pytest
from app import create_app
from db.queries import bulk_insert_application_record
from tests._sql_infos import attach_listeners

# Loads the fixtures in this module in utils to create and
# clear the unit test DB
pytest_plugins = ["fsd_utils.fixtures.db_fixtures"]
with open("tests/test_data/hand-crafted-apps.json", "r") as f:
    test_input_data = json.load(f)


@pytest.fixture(scope="function")
def seed_application_records(
    request, app, clear_test_data, enable_preserve_test_data
):
    marker = request.node.get_closest_marker("apps_to_insert")
    if marker is None:
        apps = 1
    else:
        apps = marker.args[0]
    marker = request.node.get_closest_marker("unique_fund_round")
    if marker is None:
        unique_fund_round = False
    else:
        unique_fund_round = True

    records_to_insert = []

    if unique_fund_round:
        random_fund_id = str(uuid4())
        random_round_id = str(uuid4())

    for app in apps:
        app["id"] = str(uuid4())
        if unique_fund_round:
            app["fund_id"] = random_fund_id
            app["round_id"] = random_round_id
        records_to_insert.append(app)

    # Supplied the rows we inserted for tests to use in their actions
    yield bulk_insert_application_record(records_to_insert, "COF", True)


@pytest.fixture(scope="session")
def app():
    attach_listeners()

    app = create_app()

    yield app
