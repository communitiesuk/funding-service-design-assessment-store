import copy
import json
from uuid import uuid4

import pytest
from app import create_app
from db.queries import bulk_insert_application_record
from tests._db_seed_data import load_json_strings_from_file
from tests._sql_infos import attach_listeners
from tests._sql_infos import pytest_terminal_summary  # noqa

# Loads the fixtures in this module in utils to create and
# clear the unit test DB
pytest_plugins = ["fsd_utils.fixtures.db_fixtures"]


@pytest.fixture(scope="function")
def seed_application_records(request, recreate_db, app, clear_test_data):
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
    marker = request.node.get_closest_marker("preserve_test_data")
    if marker is not None:
        request.config.cache.set("preserve_test_data", True)

    test_input_data = load_json_strings_from_file("hand-crafted-apps.json")
    records_to_insert = []

    if unique_fund_round:
        random_fund_id = str(uuid4())
        random_round_id = str(uuid4())

    for i in range(apps):
        input_data = json.loads(copy.deepcopy(test_input_data[0]))
        input_data["id"] = str(uuid4())
        if unique_fund_round:
            input_data["fund_id"] = random_fund_id
            input_data["round_id"] = random_round_id
        records_to_insert.append(input_data)

    # Supplied the rows we inserted for tests to use in their actions
    yield bulk_insert_application_record(records_to_insert, "COF", True)


@pytest.fixture(scope="session")
def app():
    attach_listeners()

    app = create_app()

    yield app
