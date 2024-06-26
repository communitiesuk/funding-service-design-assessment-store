import uuid
from datetime import datetime
from datetime import timezone

import pytest
from db.models.assessment_record.allocation_association import AllocationAssociation
from db.queries.assessment_records.queries import create_user_application_association
from db.queries.assessment_records.queries import get_user_application_associations
from db.queries.assessment_records.queries import update_user_application_association
from tests.conftest import test_input_data


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_get_users_for_application(_db, seed_application_records):
    user_id_1 = str(uuid.uuid4())
    user_id_2 = str(uuid.uuid4())
    app_id = seed_application_records[0]["application_id"]
    allocation_association_1 = AllocationAssociation(
        user_id=user_id_1,
        application_id=app_id,
        active=True,
        log={datetime.now(tz=timezone.utc).isoformat(): "activated"},
    )
    allocation_association_2 = AllocationAssociation(
        user_id=user_id_2,
        application_id=app_id,
        active=False,
        log={datetime.now(tz=timezone.utc).isoformat(): "deactivated"},
    )
    _db.session.add(allocation_association_1)
    _db.session.commit()
    _db.session.add(allocation_association_2)
    _db.session.commit()
    users = get_user_application_associations(application_id=app_id)
    assert len(users) == 2

    active_users = get_user_application_associations(application_id=app_id, active=True)
    assert len(active_users) == 1
    assert str(active_users[0].user_id) == user_id_1

    inactive_users = get_user_application_associations(application_id=app_id, active=False)
    assert len(inactive_users) == 1
    assert str(inactive_users[0].user_id) == user_id_2


@pytest.mark.apps_to_insert([{**test_input_data[0]}, {**test_input_data[1]}])
def test_get_applications_for_user(_db, seed_application_records):
    user_id = str(uuid.uuid4())
    app_id_1 = seed_application_records[0]["application_id"]
    app_id_2 = seed_application_records[1]["application_id"]
    allocation_association_1 = AllocationAssociation(
        user_id=user_id,
        application_id=app_id_1,
        active=True,
        log={datetime.now(tz=timezone.utc).isoformat(): "activated"},
    )
    allocation_association_2 = AllocationAssociation(
        user_id=user_id,
        application_id=app_id_2,
        active=False,
        log={datetime.now(tz=timezone.utc).isoformat(): "deactivated"},
    )
    _db.session.add(allocation_association_1)
    _db.session.commit()
    _db.session.add(allocation_association_2)
    _db.session.commit()
    applications = get_user_application_associations(user_id=user_id)
    assert len(applications) == 2

    active_applications = get_user_application_associations(user_id=user_id, active=True)
    assert len(active_applications) == 1
    assert str(active_applications[0].application_id) == app_id_1

    inactive_applications = get_user_application_associations(user_id=user_id, active=False)
    assert len(inactive_applications) == 1
    assert str(inactive_applications[0].application_id) == app_id_2


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_create_user_application_association(_db, seed_application_records):
    user_id = str(uuid.uuid4())
    app_id = seed_application_records[0]["application_id"]
    new_association = create_user_application_association(app_id, user_id)
    assert new_association is not None
    assert str(new_association.application_id) == app_id
    assert str(new_association.user_id) == user_id
    assert new_association.active is True
    assert "activated" == list(new_association.log.values())[0]
    try:
        datetime.fromisoformat(list(new_association.log.keys())[0])
    except ValueError:
        assert False, "log keys should be in isoformat"


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_update_user_application_association(_db, seed_application_records):
    user_id = str(uuid.uuid4())
    app_id = seed_application_records[0]["application_id"]
    create_user_application_association(app_id, user_id)
    updated_association = update_user_application_association(app_id, user_id, active=False)
    assert updated_association.active is False
    assert len(updated_association.log.keys()) == 2
    logs = [(datetime.fromisoformat(key), value) for key, value in updated_association.log.items()]

    # The timestamp for deactivated should be after activated
    assert logs[0][1] == "activated" if logs[0][0] < logs[1][0] else "deactivated"
    assert logs[1][1] == "deactivated" if logs[0][0] < logs[1][0] else "activated"


@pytest.mark.apps_to_insert([{**test_input_data[0]}])
def test_duplicate_user_application_association(_db, seed_application_records):
    user_id = str(uuid.uuid4())
    app_id = seed_application_records[0]["application_id"]
    updated_association = create_user_application_association(app_id, user_id)
    duplicate_return_value = create_user_application_association(app_id, user_id)
    assert updated_association is not None
    assert duplicate_return_value is None
