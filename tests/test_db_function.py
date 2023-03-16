import datetime
import random
import uuid
from unittest.mock import MagicMock

import pytest
import sqlalchemy
from api.routes.progress_routes import get_progress_for_applications
from db.models import Comment
from db.models import Flag
from db.models import Score
from db.models.assessment_record.assessment_records import AssessmentRecord
from db.models.assessment_record.enums import Status
from db.models.comment.enums import CommentType
from db.queries import create_flag_for_application
from db.queries import find_answer_by_key_runner
from db.queries import find_qa_complete_flag_for_applications
from db.queries import retrieve_flag_for_application
from db.queries.assessment_records.queries import (
    bulk_update_location_jsonb_blob,
)
from db.queries.assessment_records.queries import find_assessor_task_list_state
from db.queries.comments.queries import create_comment_for_application_sub_crit
from db.queries.comments.queries import get_comments_for_application_sub_crit
from db.queries.flags.queries import get_latest_flags_for_each
from db.queries.scores.queries import create_score_for_app_sub_crit
from db.queries.scores.queries import get_scores_for_app_sub_crit
from db.queries.scores.queries import get_sub_criteria_to_latest_score_map
from tests._helpers import get_assessment_record
from tests.conftest import test_input_data
from tests.test_data.flags import flag_config


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_select_field_by_id(seed_application_records):
    """test_select_field_by_id Tests that the correct field is picked from the
    corresponding application."""
    picked_row = seed_application_records[0]

    # We pick a random row to extract some data from.
    picked_app_id = picked_row["application_id"]

    picked_questions = random.choice(picked_row["jsonb_blob"]["forms"])
    picked_question = random.choice(picked_questions["questions"])
    picked_field = random.choice(picked_question["fields"])

    picked_key = picked_field["key"]

    field_found = find_answer_by_key_runner(picked_key, picked_app_id)[0]

    assert field_found == picked_field


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_jsonb_blob_immutable(_db, seed_application_records):
    """test_jsonb_blob_immutable Tests that attempting to update a json blob
    though the sqlalchemy interface raises an error.

    Error is defined in `db.models.assessment_record.db_triggers`.
    """

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    picked_row.jsonb_blob = {"application": "deleted :( oops"}

    try:
        with pytest.raises(sqlalchemy.exc.InternalError) as excinfo:

            _db.session.commit()
        assert "Cannot mutate application json" in str(excinfo.value)
    finally:
        _db.session.rollback()


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_non_blob_columns_mutable(_db, seed_application_records):
    """test_non_blob_columns_mutable Tests we haven't made the whole table
    immutable by accident when making the json blob immutable."""

    try:
        picked_row = get_assessment_record(
            seed_application_records[0]["application_id"]
        )
        picked_row.workflow_status = "IN_PROGRESS"
        _db.session.commit()
    except sqlalchemy.exc.InternalError:
        raise AssertionError
    finally:
        _db.session.rollback()


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_create_scores_for_application_sub_crit(_db, seed_application_records):
    """test_create_scores_for_application_sub_crit Tests we can create
    score records in the scores table in the appropriate format."""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    score_metadata = create_score_for_app_sub_crit(**assessment_payload)

    assert len(score_metadata) == 7
    assert score_metadata["date_created"]
    assert score_metadata["score"] == 3


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_latest_score_for_application_sub_crit(seed_application_records):
    """test_get_latest_score_for_application_sub_crit Tests we can add
    score records in the scores table and return the most recently created."""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test",
    }
    create_score_metadata = create_score_for_app_sub_crit(**assessment_payload)

    score_metadata = get_scores_for_app_sub_crit(
        application_id, sub_criteria_id
    )
    latest_score_metadata = score_metadata[0]

    assert latest_score_metadata["date_created"] == create_score_metadata.get(
        "date_created"
    )
    assert latest_score_metadata["score"] == create_score_metadata.get("score")
    assert latest_score_metadata["justification"] == create_score_metadata.get(
        "justification"
    )


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_score_history(seed_application_records):
    """test_get_score_history Tests we can get all score
    records in the scores table"""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_metadata_1 = create_score_for_app_sub_crit(
        **assessment_payload_1
    )

    assessment_payload_2 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "score": 5,
        "justification": "great",
        "user_id": "test",
    }
    create_score_metadata_2 = create_score_for_app_sub_crit(
        **assessment_payload_2
    )

    score_metadata = get_scores_for_app_sub_crit(
        application_id, sub_criteria_id, True
    )

    assert len(score_metadata) == 2
    assert score_metadata[0]["score"] == create_score_metadata_2["score"]
    assert (
        score_metadata[1]["justification"]
        == create_score_metadata_1["justification"]
    )


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_find_assessor_task_list_ui_metadata(seed_application_records):
    """test_find_assessor_task_list_ui_metadata Tests that the correct metadata
    is returned for the assessor task list UI."""

    metadata = find_assessor_task_list_state(
        seed_application_records[0]["application_id"]
    )
    assert metadata == {
        "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
        "project_name": "Mock that is used to test Assessors Task List",
        "short_id": "COF-R2W2-JWBTLN",
        "round_id": "c603d114-5364-4474-a0c4-c41cbf4d3bbd",
        "workflow_status": "NOT_STARTED",
        "date_submitted": "2022-10-27T08:32:13.383999",
        "funding_amount_requested": 4600.00,
    }


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_post_comment(seed_application_records):
    """test_post_comment tests we can create
    comment records in the comments table."""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"

    assessment_payload = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": "test",
        "theme_id": "something",
    }
    comment_metadata = create_comment_for_application_sub_crit(
        **assessment_payload
    )

    assert len(comment_metadata) == 8
    assert comment_metadata["user_id"] == "test"
    assert comment_metadata["theme_id"] == "something"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_comments(seed_application_records):
    """test_get_comments tests we can get all comment
    records in the comments table filtered by application_id,
    subcriteria_id and theme_id"""

    picked_row = get_assessment_record(
        seed_application_records[0]["application_id"]
    )
    application_id = picked_row.application_id
    sub_criteria_id = "app-info"
    theme_id = "theme"

    assessment_payload_1 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": "test",
        "theme_id": theme_id,
    }
    create_comment_for_application_sub_crit(**assessment_payload_1)

    assessment_payload_2 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": "test",
        "theme_id": theme_id,
    }
    create_comment_for_application_sub_crit(**assessment_payload_2)

    assessment_payload_3 = {
        "application_id": application_id,
        "sub_criteria_id": sub_criteria_id,
        "comment": "Please provide more information",
        "comment_type": "COMMENT",
        "user_id": "test",
        "theme_id": "different theme",
    }
    create_comment_for_application_sub_crit(**assessment_payload_3)

    comment_metadata_for_theme = get_comments_for_application_sub_crit(
        application_id, sub_criteria_id, theme_id
    )
    assert len(comment_metadata_for_theme) == 2
    assert (
        comment_metadata_for_theme[0]["theme_id"]
        == comment_metadata_for_theme[1]["theme_id"]
    )

    comment_metadata_no_theme = get_comments_for_application_sub_crit(
        application_id, sub_criteria_id, theme_id=None
    )
    assert len(comment_metadata_no_theme) == 3

    # TODO: remove this once frontend is updated not to use 'theme_id=score'
    comment_metadata_score_theme_id = get_comments_for_application_sub_crit(
        application_id, sub_criteria_id, theme_id="score"
    )
    assert len(comment_metadata_score_theme_id) == 3


@pytest.mark.apps_to_insert(test_input_data)
def test_get_progress_for_applications(seed_application_records):
    """test_create_scores_for_application_sub_crit Tests we can create
    score records in the scores table in the appropriate format."""

    application_id_1 = seed_application_records[0]["application_id"]
    application_id_2 = seed_application_records[1]["application_id"]
    sub_criteria_ids = ["benefits", "engagement"]

    score_payload_1 = {
        "application_id": application_id_1,
        "sub_criteria_id": sub_criteria_ids[0],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_1)

    score_payload_2 = {
        "application_id": application_id_1,
        "sub_criteria_id": sub_criteria_ids[1],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_2)

    score_payload_3 = {
        "application_id": application_id_2,
        "sub_criteria_id": sub_criteria_ids[1],
        "score": 3,
        "justification": "bang average",
        "user_id": "test",
    }
    create_score_for_app_sub_crit(**score_payload_3)

    request = MagicMock()
    request.get_json.return_value = {
        "application_ids": [
            application_id_1,
            application_id_2,
        ]
    }
    application_progress_list = get_progress_for_applications(
        [application_id_1, application_id_2]
    )

    assert len(application_progress_list) == 2
    for application in application_progress_list:
        if application["application_id"] == application_id_1:
            assert application["progress"] == 20
        if application["application_id"] == application_id_2:
            assert application["progress"] == 10


@pytest.mark.parametrize(
    "insertion_object",
    [
        Score(
            application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
            sub_criteria_id="test",
            user_id="test",
            score=5,
            justification="great",
        ),
        Comment(
            application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
            sub_criteria_id="test",
            user_id="test",
            comment="great",
            comment_type=CommentType.COMMENT,
        ),
    ],
)
@pytest.mark.apps_to_insert(test_input_data)
def test_update_workflow_status_on_insert(
    _db, insertion_object, seed_application_records
):
    application_id = seed_application_records[0]["application_id"]
    assessment_record = (
        _db.session.query(AssessmentRecord)
        .where(AssessmentRecord.application_id == application_id)
        .first()
    )

    assert assessment_record.workflow_status == Status.NOT_STARTED

    insertion_object.application_id = application_id
    _db.session.add(insertion_object)
    _db.session.commit()

    assert assessment_record.workflow_status == Status.IN_PROGRESS


@pytest.fixture
def sample_flags(_db):
    flags = []
    for config in flag_config:
        flag = Flag(**config)
        flags.append(flag)
        _db.session.add(flag)
    _db.session.commit()

    yield (flags)

    for flag in flags:
        _db.session.delete(flag)
    _db.session.commit()


@pytest.mark.apps_to_insert([test_input_data[0]])
@pytest.mark.parametrize("flag_config", flag_config)
def test_create_flag_for_application(flag_config, seed_application_records):
    flag = Flag(**flag_config)
    result = create_flag_for_application(
        application_id=seed_application_records[0]["application_id"],
        **flag_config,
    )
    #     justification=flag.justification,
    #     section_to_flag=flag.section_to_flag,
    #     application_id=seed_application_records[0]["application_id"],
    #     user_id=flag.user_id,
    #     flag_type=flag.flag_type,
    # )

    assert result["justification"] == flag.justification
    assert result["section_to_flag"] == flag.section_to_flag
    assert (
        result["application_id"]
        == seed_application_records[0]["application_id"]
    )
    assert result["user_id"] == flag.user_id
    assert result["flag_type"] == flag.flag_type.name


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_retrieve_flag_for_application(_db, seed_application_records):
    """Put two flags for the same application and expect the most
    recent flag to be retuned for the application."""
    now = datetime.datetime.now()
    earlier = now - datetime.timedelta(days=1)
    first_flag = Flag(
        application_id=seed_application_records[0]["application_id"],
        date_created=earlier,
        **flag_config[0],
    )
    _db.session.add(first_flag)
    second_flag = Flag(
        application_id=seed_application_records[0]["application_id"],
        date_created=now,
        **flag_config[1],
    )
    _db.session.add(second_flag)
    _db.session.commit()
    result = retrieve_flag_for_application(
        seed_application_records[0]["application_id"]
    )

    assert result["justification"] == second_flag.justification
    assert result["section_to_flag"] == second_flag.section_to_flag
    assert result["application_id"] == second_flag.application_id
    assert result["user_id"] == second_flag.user_id
    assert result["flag_type"] == second_flag.flag_type.name


@pytest.mark.apps_to_insert(test_input_data)
def test_find_qa_complete_flag_for_applications(_db, seed_application_records):
    """Put QA_COMPLETED flags in 2 out of 3 applications and
    only retrieve the metadata for the 1 with QA_COMPLETED"""

    first_application_flagged_flag = Flag(
        application_id=seed_application_records[0]["application_id"],
        **flag_config[2],
    )
    _db.session.add(first_application_flagged_flag)

    first_application_qa_complete_flag = Flag(
        application_id=seed_application_records[0]["application_id"],
        **flag_config[3],
    )
    _db.session.add(first_application_qa_complete_flag)

    second_application_qa_complete_flag = Flag(
        application_id=seed_application_records[1]["application_id"],
        **flag_config[4],
    )
    _db.session.add(second_application_qa_complete_flag)

    third_application_flagged_flag = Flag(
        application_id=seed_application_records[2]["application_id"],
        **flag_config[0],
    )
    _db.session.add(third_application_flagged_flag)

    _db.session.commit()

    result = find_qa_complete_flag_for_applications(
        [
            first_application_flagged_flag.application_id,
            second_application_qa_complete_flag.application_id,
            third_application_flagged_flag.application_id,
        ]
    )

    assert (
        result[0]["application_id"]
        == first_application_flagged_flag.application_id
    )
    assert (
        result[0]["flag_type"] == first_application_flagged_flag.flag_type.name
    )
    assert (
        result[1]["application_id"]
        == second_application_qa_complete_flag.application_id
    )
    assert (
        result[1]["flag_type"]
        == second_application_qa_complete_flag.flag_type.name
    )
    assert len(result) == 2


@pytest.mark.skip(reason="integrate flags into seeded data")
def test_get_latest_flags_for_each(sample_flags):
    result_list = get_latest_flags_for_each()

    assert len(result_list) == 3
    assert result_list[0]["justification"] == "Latest 1"
    assert result_list[1]["justification"] == "Latest 2"
    assert result_list[2]["justification"] == "Latest 3"


@pytest.mark.skip(reason="integrate flags into seeded data")
def test_get_latest_flags_for_each_with_type_filter(sample_flags):
    result_list = get_latest_flags_for_each("QA_COMPLETED")

    assert len(result_list) == 1
    assert result_list[0]["flag_type"] == "QA_COMPLETED"


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_get_sub_criteria_to_latest_score_map(_db, seed_application_records):
    application_id = seed_application_records[0]["application_id"]
    sub_criteria_1_id = str(uuid.uuid4())
    sub_criteria_2_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    now = datetime.datetime.now()
    earlier = now - datetime.timedelta(days=1)
    latest = now + datetime.timedelta(days=1)

    scores = [
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=2,
            justification="test",
            date_created=earlier,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=5,
            justification="test",
            date_created=now,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_1_id,
            score=2,
            justification="test",
            date_created=latest,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=1,
            justification="test",
            date_created=earlier,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=3,
            justification="test",
            date_created=now,
            user_id=user_id,
        ),
        Score(
            application_id=application_id,
            sub_criteria_id=sub_criteria_2_id,
            score=5,
            justification="test",
            date_created=latest,
            user_id=user_id,
        ),
    ]
    _db.session.add_all(scores)
    _db.session.commit()

    result = get_sub_criteria_to_latest_score_map(str(application_id))

    assert result[sub_criteria_1_id] == 2
    assert result[sub_criteria_2_id] == 5


@pytest.mark.apps_to_insert([test_input_data[0]])
def test_bulk_update_location_data(_db, seed_application_records):
    application_id = seed_application_records[0]["application_id"]

    test_random_append = random.randint(999, 99999)

    location = {
        "error": False,
        "county": f"test_county_{test_random_append}",
        "country": f"test_country_{test_random_append}",
    }

    application_ids_to_location_data = [
        {"application_id": application_id, "location": location}
    ]

    bulk_update_location_jsonb_blob(application_ids_to_location_data)

    assessment_record = (
        _db.session.query(AssessmentRecord)
        .where(AssessmentRecord.application_id == application_id)
        .first()
    )
    assert location == assessment_record.location_json_blob


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
