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
from db.queries import retrieve_flag_for_application
from db.queries import find_qa_complete_flag_for_applications
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
from tests._helpers import get_random_row
from tests.test_data.flags import flag_config


def test_select_field_by_id():
    """test_select_field_by_id Tests that the correct field is picked from the
    corresponding application."""
    picked_row = get_random_row(AssessmentRecord)

    # We pick a random row to extract some data from.
    picked_app_id = picked_row.application_id

    picked_questions = random.choice(picked_row.jsonb_blob["forms"])
    picked_question = random.choice(picked_questions["questions"])
    picked_field = random.choice(picked_question["fields"])

    picked_key = picked_field["key"]

    field_found = find_answer_by_key_runner(picked_key, picked_app_id)[0]

    assert field_found == picked_field


def test_jsonb_blob_immutable(db_session):
    """test_jsonb_blob_immutable Tests that attempting to update a json blob
    though the sqlalchemy interface raises an error.

    Error is defined in `db.models.assessment_record.db_triggers`.
    """

    picked_row = get_random_row(AssessmentRecord)
    picked_row.jsonb_blob = {"application": "deleted :( oops"}

    try:
        db_session.commit()
    except sqlalchemy.exc.InternalError as error:
        assert "Cannot mutate application json" in str(error)
    else:
        assert False


def test_non_blob_columns_mutable(db_session):
    """test_non_blob_columns_mutable Tests we haven't made the whole table
    immutable by accident when making the json blob immutable."""

    try:
        picked_row = get_random_row(AssessmentRecord)
        picked_row.workflow_status = "IN_PROGRESS"
        db_session.commit()
    except sqlalchemy.exc.InternalError:
        raise AssertionError


def test_create_scores_for_application_sub_crit():
    """test_create_scores_for_application_sub_crit Tests we can create
    score records in the scores table in the appropriate format."""

    picked_row = get_random_row(AssessmentRecord)
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


def test_get_latest_score_for_application_sub_crit():
    """test_get_latest_score_for_application_sub_crit Tests we can add
    score records in the scores table and return the most recently created."""

    picked_row = get_random_row(AssessmentRecord)
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


def test_get_score_history():
    """test_get_score_history Tests we can get all score
    records in the scores table"""

    picked_row = get_random_row(AssessmentRecord)
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
    assert score_metadata[0]["score"] == create_score_metadata_1["score"]
    assert (
        score_metadata[1]["justification"]
        == create_score_metadata_2["justification"]
    )


def test_find_assessor_task_list_ui_metadata():
    """test_find_assessor_task_list_ui_metadata Tests that the correct metadata
    is returned for the assessor task list UI."""

    metadata = find_assessor_task_list_state(
        "a3ec41db-3eac-4220-90db-c92dea049c00"
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


def test_post_comment():
    """test_post_comment tests we can create
    comment records in the comments table."""

    picked_row = get_random_row(AssessmentRecord)
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


def test_get_comments():
    """test_get_comments tests we can get all comment
    records in the comments table filtered by application_id,
    subcriteria_id and theme_id"""

    picked_row = get_random_row(AssessmentRecord)
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
    comment_metadata = get_comments_for_application_sub_crit(
        application_id, sub_criteria_id, theme_id="score"
    )

    assert len(comment_metadata_for_theme) == 2
    assert (
        comment_metadata_for_theme[0]["theme_id"]
        == comment_metadata_for_theme[1]["theme_id"]
    )
    assert len(comment_metadata) == 3


def test_get_progress_for_applications(monkeypatch):
    """test_create_scores_for_application_sub_crit Tests we can create
    score records in the scores table in the appropriate format."""

    picked_row = get_random_row(AssessmentRecord)
    application_id_1 = picked_row.application_id
    picked_row = get_random_row(AssessmentRecord)
    application_id_2 = picked_row.application_id
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
def test_update_workflow_status_on_insert(db_session, insertion_object):
    assessment_record = (
        db_session.query(AssessmentRecord)
        .where(
            AssessmentRecord.application_id
            == "a3ec41db-3eac-4220-90db-c92dea049c01"
        )
        .first()
    )

    assert assessment_record.workflow_status == Status.NOT_STARTED

    db_session.add(insertion_object)
    db_session.commit()

    assert assessment_record.workflow_status == Status.IN_PROGRESS


@pytest.fixture
def sample_flags(db_session):
    flags = []
    for config in flag_config:
        flag = Flag(**config)
        flags.append(flag)
        db_session.add(flag)
    db_session.commit()

    yield (flags)

    for flag in flags:
        db_session.delete(flag)
    db_session.commit()


@pytest.mark.parametrize("flag_config", flag_config)
def test_create_flag_for_application(flag_config):
    flag = Flag(**flag_config)
    result = create_flag_for_application(
        justification=flag.justification,
        section_to_flag=flag.section_to_flag,
        application_id=flag.application_id,
        user_id=flag.user_id,
        flag_type=flag.flag_type,
    )

    assert result["justification"] == flag.justification
    assert result["section_to_flag"] == flag.section_to_flag
    assert result["application_id"] == flag.application_id
    assert result["user_id"] == flag.user_id
    assert result["flag_type"] == flag.flag_type.name


def test_retrieve_flag_for_application(db_session):
    """Put two flags for the same application and expect the most
    recent flag to be retuned for the application."""
    first_flag = Flag(**flag_config[1])
    db_session.add(first_flag)
    second_flag = Flag(**flag_config[0])
    db_session.add(second_flag)
    db_session.commit()
    result = retrieve_flag_for_application(first_flag.application_id)

    assert result["justification"] == second_flag.justification
    assert result["section_to_flag"] == second_flag.section_to_flag
    assert result["application_id"] == second_flag.application_id
    assert result["user_id"] == second_flag.user_id
    assert result["flag_type"] == second_flag.flag_type.name

def test_find_qa_complete_flag_for_applications(db_session):
    """Put QA_COMPLETED flags in 1 out of 2 applications and
    only retrieve the metadata for the 1 with QA_COMPLETED"""

    first_flag = Flag(**flag_config[2])
    db_session.add(first_flag)
    second_flag = Flag(**flag_config[3])

    db_session.add(second_flag)
    third_flag = Flag(**flag_config[0])
    db_session.add(third_flag)

    db_session.commit()

    result = find_qa_complete_flag_for_applications([first_flag.application_id, third_flag.application_id])

    assert result[0]['application_id'] == first_flag.application_id
    assert result[0]['flag_type'] == first_flag.flag_type.name
    assert len(result) == 1


def test_get_latest_flags_for_each(sample_flags):
    result_list = get_latest_flags_for_each()

    assert len(result_list) == 3
    assert result_list[0]["justification"] == "Latest 1"
    assert result_list[1]["justification"] == "Latest 2"
    assert result_list[2]["justification"] == "Latest 3"


def test_get_latest_flags_for_each_with_type_filter(sample_flags):
    result_list = get_latest_flags_for_each("QA_COMPLETED")

    assert len(result_list) == 1
    assert result_list[0]["flag_type"] == "QA_COMPLETED"


def test_get_sub_criteria_to_latest_score_map(db_session):
    application_id = "a3ec41db-3eac-4220-90db-c92dea049c01"
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
    db_session.add_all(scores)
    db_session.commit()

    result = get_sub_criteria_to_latest_score_map(str(application_id))

    assert result[sub_criteria_1_id] == 2
    assert result[sub_criteria_2_id] == 5


def test_bulk_update_location_data(db_session):
    picked_row = get_random_row(AssessmentRecord)
    assert picked_row, "Picked row not returned"
    application_id = picked_row.application_id

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
        db_session.query(AssessmentRecord)
        .where(AssessmentRecord.application_id == application_id)
        .first()
    )
    assert location == assessment_record.location_json_blob
