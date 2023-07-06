from uuid import uuid4

import pytest
from api.routes.tag_routes import get_tags_for_fund_round
from db.queries.tags.queries import insert_tags

tags_correct_format = [
    {
        "value": "Test tag 1",
        "tag_creator_user_id": "Test User",
        "colour": "GREEN",
    },
    {
        "value": "Not recommended",
        "tag_creator_user_id": "Test User",
    },
    {
        "value": "For discussion",
        "tag_creator_user_id": "Test User",
    },
    {
        "value": "Incomplete - not for review",
        "tag_creator_user_id": "Test User",
    },
]

tag_values = [x["value"] for x in tags_correct_format]

tags_incorrect_format = [
    {
        "key": "Test tag 1",
        "colour": "Green",
        "tag_creator_user_id": "Test User",
    },
    {
        "value": "Not recommended",
        "species": "silk",
        "tag_creator_user_id": "Test User",
    },
    {
        "value": "For discussion",
        "tag_creator_user_id": "Test User",
    },
    {
        "value": "Incomplete - not for review",
        "tag_creator_user_id": "Test User",
    },
]

tags_incorrect_colour = [
    {
        "value": "Test tag 1",
        "colour": "Green",
        "tag_creator_user_id": "Test User",
    },
]


def test_insert_tags(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    result = insert_tags(tags_correct_format, fund_id_test, round_id_test)
    assert len(result) == 4
    assert result[0][1] in tag_values
    # Test default colour is set to NONE if not included in tag config
    assert "NONE" == result[2][3].name


def test_insert_tags_twice_ignores_second_duplicates(_db):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    insert_tags(tags_correct_format, fund_id_test, round_id_test)

    with pytest.raises(Exception) as e_info:
        insert_tags(tags_correct_format, fund_id_test, round_id_test)

    assert "duplicate key value violates" in str(e_info.value.orig.pgerror)


def test_insert_tags_bad_tag_format(_db):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    with pytest.raises(KeyError):
        insert_tags(tags_incorrect_format, fund_id_test, round_id_test)
    # This operation cleans up the session resources and ensures that
    # the session is properly closed following the raised error.
    _db.session.remove()


def test_insert_tag_with_unknown_colour_fails(_db):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())

    with pytest.raises(Exception) as e_info:
        insert_tags(tags_incorrect_colour, fund_id_test, round_id_test)

    assert "invalid input value for enum colour" in str(
        e_info.value.orig.pgerror
    )
    # This operation cleans up the session resources and ensures
    # that the session is properly closed following the raised error.
    _db.session.remove()


def test_get_tags(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    insert_tags(tags_correct_format, fund_id_test, round_id_test)
    result = get_tags_for_fund_round(fund_id_test, round_id_test)
    assert len(result) == 4
    assert result[0]["value"] in tag_values
    assert all(
        key in result[0].keys()
        for key in [
            "round_id",
            "creator_user_id",
            "fund_id",
            "colour",
            "created_at",
            "value",
            "id",
            "active",
        ]
    )
