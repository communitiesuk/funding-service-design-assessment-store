from uuid import uuid4

import pytest
from api.routes.tag_routes import get_tags_for_fund_round
from db.queries.tags.queries import insert_tags

# _db.session.remove()
# This operation cleans up the session resources and ensures that
# the session is properly closed following the raised error.

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

tags_correct_format2 = [
    {
        "value": "Test tag 2",
        "tag_creator_user_id": "Test User",
        "colour": "GREEN",
    },
    {
        "value": "Not recommended 2",
        "tag_creator_user_id": "Test User",
    },
    {
        "value": "For discussion 2",
        "tag_creator_user_id": "Test User",
    },
    {
        "value": "Incomplete - not for review 2",
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
    assert [tag.value in tag_values for tag in result]
    # Test default colour is set to NONE if not included in tag config
    assert [tag.colour.name in ["NONE", "GREEN"] for tag in result]


def test_insert_tags_fails_for_tag_with_special_chars(_db, clear_test_data):
    tag_special_chars = [
        {
            "value": "Test tag 1 !£",
            "tag_creator_user_id": "Test User",
            "colour": "GREEN",
        }
    ]
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    with pytest.raises(ValueError) as e_info:
        insert_tags(tag_special_chars, fund_id_test, round_id_test)
    assert (
        "The value should only contain apostrophes, hyphens, letters, digits, and spaces."
        in str(e_info.value)
    )
    _db.session.remove()


def test_insert_tags_twice_fails(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    insert_tags(tags_correct_format2, fund_id_test, round_id_test)

    with pytest.raises(Exception) as e_info:
        insert_tags(tags_correct_format, fund_id_test, round_id_test)

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_duplicate_tags_same_payload_fails(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    same_tags_with_different_cases = [
        {
            "value": "same",
            "tag_creator_user_id": "Test User",
            "colour": "GREEN",
        },
        {
            "value": "same",
            "tag_creator_user_id": "Test User",
            "colour": "GREEN",
        },
    ]

    with pytest.raises(Exception) as e_info:
        insert_tags(
            same_tags_with_different_cases, fund_id_test, round_id_test
        )

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_duplicate_tags_not_case_sensitive_fails(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    same_tags_with_different_cases = [
        {
            "value": "look at the case",
            "tag_creator_user_id": "Test User",
            "colour": "GREEN",
        },
        {
            "value": "LOOK AT THE CASE",
            "tag_creator_user_id": "Test User",
            "colour": "GREEN",
        },
    ]

    with pytest.raises(Exception) as e_info:
        insert_tags(
            same_tags_with_different_cases, fund_id_test, round_id_test
        )

    assert "duplicate key value violates" in str(e_info.value)
    _db.session.remove()


def test_insert_tags_bad_tag_format(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())
    with pytest.raises(Exception) as e_info:
        insert_tags(tags_incorrect_format, fund_id_test, round_id_test)

    assert "'NoneType' object has no attribute 'strip" in str(e_info.value)
    _db.session.remove()


def test_insert_tag_with_unknown_colour_fails(_db, clear_test_data):
    fund_id_test = str(uuid4())
    round_id_test = str(uuid4())

    with pytest.raises(Exception) as e_info:
        insert_tags(tags_incorrect_colour, fund_id_test, round_id_test)

    assert "invalid input value for enum colour" in str(e_info.value)
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
