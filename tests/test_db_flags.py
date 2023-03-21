import pytest
from db.models import Flag
from db.models.assessment_record.assessment_records import AssessmentRecord
from db.models.assessment_record.enums import Status
from db.queries import create_flag_for_application
from db.queries import find_qa_complete_flag_for_applications
from db.queries import retrieve_flag_for_application
from db.queries.flags.queries import get_latest_flags_for_each
from tests.conftest import test_input_data
from tests.test_data.flags import flag_config


@pytest.mark.apps_to_insert([test_input_data[0]])
@pytest.mark.parametrize("flag_config", flag_config)
def test_create_flag_for_application(flag_config, seed_application_records):
    flag = Flag(**flag_config)
    result = create_flag_for_application(
        application_id=seed_application_records[0]["application_id"],
        justification=flag.justification,
        section_to_flag=flag.section_to_flag,
        user_id=flag.user_id,
        flag_type=flag.flag_type,
    )

    assert result["justification"] == flag.justification
    assert result["section_to_flag"] == flag.section_to_flag
    assert (
        result["application_id"]
        == seed_application_records[0]["application_id"]
    )
    assert result["user_id"] == flag.user_id
    assert result["flag_type"] == flag.flag_type.name


@pytest.mark.apps_to_insert(
    [{**test_input_data[0], "flags": flag_config[0:2]}]
)
def test_retrieve_flag_for_application(_db, seed_application_records):
    """Put two flags for the same application and expect the most
    recent flag to be retuned for the application."""
    # now = datetime.datetime.now()
    # earlier = now - datetime.timedelta(days=1)
    # first_flag = Flag(
    #     application_id=seed_application_records[0]["application_id"],
    #     **flag_config[0],
    # )
    # _db.session.add(first_flag)
    # second_flag = Flag(
    #     application_id=seed_application_records[0]["application_id"],
    #     **flag_config[1],
    # )
    # _db.session.add(second_flag)
    # _db.session.commit()
    result = retrieve_flag_for_application(
        seed_application_records[0]["application_id"]
    )

    assert result["justification"] == "Latest 1"
    assert result["section_to_flag"] == "Test section 1"
    assert (
        result["application_id"]
        == seed_application_records[0]["application_id"]
    )
    # assert result["user_id"] == second_flag.user_id
    # assert result["flag_type"] == second_flag.flag_type.name


@pytest.mark.apps_to_insert(
    [
        {**test_input_data[0], "flags": [flag_config[2], flag_config[3]]},
        {**test_input_data[1], "flags": [flag_config[4]]},
        {**test_input_data[2], "flags": [flag_config[0]]},
    ]
)
def test_find_qa_complete_flag_for_applications(_db, seed_application_records):
    """Put QA_COMPLETED flags in 2 out of 3 applications and
    only retrieve the metadata for the 1 with QA_COMPLETED"""

    result = find_qa_complete_flag_for_applications(
        [app["application_id"] for app in seed_application_records]
    )

    assert len(result) == 2
    assert (
        result[0]["application_id"]
        == seed_application_records[0]["application_id"]
    )
    assert result[0]["flag_type"] == "QA_COMPLETED"
    assert (
        result[1]["application_id"]
        == seed_application_records[1]["application_id"]
    )
    assert result[1]["flag_type"] == "QA_COMPLETED"


# TODO Remove skip once get_latest_flags_for_each can filter on fund/round id.
# In the meantime, will work if run in isolation
@pytest.mark.skip(reason="Filter on fund and round id")
@pytest.mark.apps_to_insert(
    [
        {**test_input_data[0], "flags": [flag_config[0], flag_config[1]]},
        {**test_input_data[1], "flags": [flag_config[2], flag_config[3]]},
        {**test_input_data[2], "flags": [flag_config[4], flag_config[5]]},
    ]
)
@pytest.mark.unique_fund_round(True)
def test_get_latest_flags_for_each(seed_application_records):
    result_list = get_latest_flags_for_each()

    assert len(result_list) == 3
    assert result_list[0]["justification"] == "Latest 1"
    assert result_list[1]["justification"] == "Latest 2"
    assert result_list[2]["justification"] == "Latest 3"


# TODO Remove skip once get_latest_flags_for_each can filter on fund/round id.
# In the meantime, will work if run in isolation
@pytest.mark.skip(reason="Filter on fund and round id")
@pytest.mark.apps_to_insert(
    [
        {**test_input_data[0], "flags": [flag_config[0], flag_config[1]]},
        {**test_input_data[1], "flags": [flag_config[2], flag_config[3]]},
        {**test_input_data[2], "flags": [flag_config[4], flag_config[5]]},
    ]
)
def test_get_latest_flags_for_each_with_type_filter(seed_application_records):
    result_list = get_latest_flags_for_each("QA_COMPLETED")

    assert len(result_list) == 1
    assert result_list[0]["flag_type"] == "QA_COMPLETED"


@pytest.mark.skip(reason="integrate flags into seeded data")
@pytest.mark.parametrize(
    "status_or_flag, expected_application_count",
    [
        (
            "NOT_STARTED",
            1,
        ),
        (
            "IN_PROGRESS",
            1,
        ),
        (
            "COMPLETED",
            1,
        ),
        (
            "FLAGGED",
            2,
        ),
        (
            "STOPPED",
            0,
        ),
        (
            "QA_COMPLETED",
            2,
        ),
        (
            "UNKNOWN_STATUS_OR_FLAG",
            3,
        ),
    ],
)
def test_get_most_recent_metadata_statuses_for_fund_round_id(
    _db, sample_flags, status_or_flag, expected_application_count
):
    from db.queries.assessment_records.queries import (
        get_metadata_for_fund_round_id,
    )

    assessment_record_A = (
        _db.session.query(AssessmentRecord)
        .where(
            AssessmentRecord.application_id
            == "a3ec41db-3eac-4220-90db-c92dea049c01"
        )
        .first()
    )

    assessment_record_A.workflow_status = Status.IN_PROGRESS

    assessment_record_B = (
        _db.session.query(AssessmentRecord)
        .where(
            AssessmentRecord.application_id
            == "c3ec41db-3eac-4220-90db-c92dea049c03"
        )
        .first()
    )

    assessment_record_B.workflow_status = Status.COMPLETED

    metadata = get_metadata_for_fund_round_id(
        "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
        "",
        "",
        status_or_flag,
    )
    assert len(metadata) == expected_application_count
