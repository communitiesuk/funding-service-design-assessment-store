import pytest
from db.models.assessment_record import AssessmentRecord
from db.queries.assessment_records.queries import set_tags_for_application
from sqlalchemy import select
from tests.conftest import test_input_data


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_set_tags_all_new(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )
    app = _db.session.scalars(stmt).one()
    assert len(app.tags) == 0

    new_tags = ["tag_1", "tag_2"]
    set_tags_for_application(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tags) == len(new_tags)
    assert all(item in new_tags for item in [t.tag_value for t in app.tags])


@pytest.mark.apps_to_insert(
    [{**test_input_data[0], "app_tags": ["old_tag_1", "old_tag_2"]}]
)
def test_set_tags_add_and_remove(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )

    new_tags = ["tag_1", "tag_2"]
    set_tags_for_application(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tags) == len(new_tags)
    assert all(item in new_tags for item in [t.tag_value for t in app.tags])


@pytest.mark.apps_to_insert(
    [{**test_input_data[0], "app_tags": ["old_tag_1", "old_tag_2"]}]
)
def test_set_tags_only_add(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )

    new_tags = ["old_tag_1", "old_tag_2", "new_tag_3"]
    set_tags_for_application(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tags) == len(new_tags)
    assert all(item in new_tags for item in [t.tag_value for t in app.tags])


@pytest.mark.apps_to_insert(
    [{**test_input_data[0], "app_tags": ["old_tag_1", "old_tag_2"]}]
)
def test_set_tags_remove_all(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )

    new_tags = []
    set_tags_for_application(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tags) == len(new_tags)
    assert all(item in new_tags for item in [t.tag_value for t in app.tags])


@pytest.mark.apps_to_insert(
    [{**test_input_data[0], "app_tags": ["old_tag_1", "old_tag_2"]}]
)
def test_set_tags_unchanged(_db, seed_application_records):
    app_id = seed_application_records[0]["application_id"]
    stmt = select(AssessmentRecord).where(
        AssessmentRecord.application_id == app_id
    )

    new_tags = ["old_tag_1", "old_tag_2"]
    set_tags_for_application(app_id, new_tags)

    app = _db.session.scalars(stmt).one()
    assert len(app.tags) == len(new_tags)
    assert all(item in new_tags for item in [t.tag_value for t in app.tags])
