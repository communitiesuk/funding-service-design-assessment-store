import copy
import json
from uuid import uuid4

import pytest
from app import create_app
from db.queries import bulk_insert_application_record
from fsd_utils.fixtures.db_fixtures import prep_db
from tests._db_seed_data import get_dynamic_rows
from tests._db_seed_data import load_json_strings_from_file
from tests._sql_infos import attach_listeners
from tests._sql_infos import pytest_terminal_summary  # noqa

pytest_plugins = ["fsd_utils.fixtures.db_fixtures"]


def row_data(
    apps_per_round, rounds_per_fund, number_of_funds, fund_round_config
):
    """row_data A fixture which provides the test row data."""

    row_data = list(
        get_dynamic_rows(
            apps_per_round, rounds_per_fund, number_of_funds, fund_round_config
        )
    )

    return row_data


def seed_database_randomly(apps_per_round, rounds_per_fund, number_of_funds):
    test_input_data = row_data(
        apps_per_round, rounds_per_fund, number_of_funds
    )

    bulk_insert_application_record(test_input_data, "COF")


def seed_database_for_fund_round(apps_per_round, fund_round_config):
    test_input_data = row_data(apps_per_round, 1, 1, fund_round_config)

    bulk_insert_application_record(test_input_data, "COF")


def seed_handcrafted_data():
    test_input_data = load_json_strings_from_file("hand-crafted-apps.json")

    bulk_insert_application_record(test_input_data, "COF")


def seed_database_deterministically():
    test_input_data = load_json_strings_from_file("apps.json")

    bulk_insert_application_record(test_input_data, "COF")


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
    yield bulk_insert_application_record(records_to_insert, "COF", True)


@pytest.fixture(scope="session")
def app():
    attach_listeners()

    app = create_app()

    yield app


@pytest.fixture(scope="session")
def _db(app, request):
    yield app.extensions["sqlalchemy"]


@pytest.fixture(scope="session")
def recreate_db(request, _db, app):
    reuse_db = bool(request.config.cache.get("reuse_db", False))
    with app.app_context():
        prep_db(reuse_db)
    request.config.cache.set("reuse_db", True)
    yield


@pytest.fixture(scope="module")
def clear_test_data(app, _db, request):
    """
    Fixture to clean up the database after each test.

    This fixture clears the database by deleting all data
    from tables and disabling foreign key checks before the test,
    and resetting foreign key checks after the test.

    """
    with app.app_context():

        yield
        marker = request.node.get_closest_marker("preserve_test_data")
        if marker is None:
            # rollback incase of any errors during test session
            _db.session.rollback()
            # disable foreign key checks
            _db.session.execute("SET session_replication_role = replica")
            # delete all data from tables
            for table in reversed(_db.metadata.sorted_tables):
                _db.session.execute(table.delete())
            # reset foreign key checks
            _db.session.execute("SET session_replication_role = DEFAULT")
            _db.session.commit()
        else:
            # If test requests 'preserve test data' make sure
            # on the next run we clear out the DB completely.
            request.config.cache.set("reuse_db", False)


def pytest_addoption(parser):
    parser.addoption(
        "--apps-per-round",
        action="store",
        default=100,
        help="The amount of rows to use when testing the db.",
        type=int,
    )
    parser.addoption(
        "--rounds-per-fund",
        action="store",
        default=2,
        help="The amount of rows to use when testing the db.",
        type=int,
    )
    parser.addoption(
        "--number-of-funds",
        action="store",
        default=5,
        help="The amount of rows to use when testing the db.",
        type=int,
    )
    parser.addoption(
        "--statementdetails",
        action="store",
        default=True,
        help="The amount of rows to use when testing the db.",
        type=bool,
    )
    parser.addoption(
        "--randomdata",
        action="store",
        default=False,
        help="Decides if random data is used to seed the application rows..",
        type=bool,
    )
