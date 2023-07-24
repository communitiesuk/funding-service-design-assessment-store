from typing import List

from db import db
from db.models.tag.tag_types import TagType
from db.models.tag.tags import Tag
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound


def insert_tags(tags, fund_id, round_id):
    """
    Inserts tags associated with a round.

    Args:
        tags (list): A list of tag dictionaries [{
                "value": "",
                "purpose": "",
                "creator_user_id": "",
            }]
        round_id (str): The round to insert tags for.
        fund_id (str): The fund to insert tags for.

    Returns:
        inserted_tags (list): This method returns a list of inserted tags (the tag id and key)
    """
    inserted_tags = []
    for tag_data in tags:
        value = tag_data.get("value")
        creator_user_id = tag_data.get("creator_user_id")
        tag_type_id = tag_data.get("tag_type_id")

        # Create a new tag instance and trigger validation
        tag = Tag(
            value=value,
            fund_id=fund_id,
            round_id=round_id,
            creator_user_id=creator_user_id,
            type_id=tag_type_id,
        )
        db.session.add(tag)

        try:
            db.session.flush()  # Flush changes to trigger validation
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(
                f"Error inserting tag '{value}': {str(e)}"
            )
            raise ValueError(f"Error inserting tag '{value}': {str(e)}")

        inserted_tags.append(tag)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error inserting tags: {str(e)}")
        raise ValueError(f"Error inserting tags: {str(e)}")
    return inserted_tags


def update_tags(tags, fund_id, round_id):
    """
    Takes a list of tag updates and applies them to the tag_id specified.

    Args:
        tags (list): A list of tag update dictionaries [{
                "id": "",
                "value": "",
                "purpose": "",
                "creator_user_id": "",
                "active": "",
            }]
        round_id (str): The round to insert tags for.
        fund_id (str): The fund to insert tags for.

    Returns:
        updated (list): This method returns a list of updated tags (the tag id and key)
    """
    updated_tags = []

    for tag_data in tags:
        tag_id = tag_data["id"]
        tag_value = tag_data.get("value")
        tag_type_id = tag_data.get("tag_type_id")
        creator_user_id = tag_data.get("creator_user_id")
        active_status = tag_data.get("active")

        try:
            # Check if the tag already exists in the database
            tag = (
                db.session.query(Tag)
                .filter_by(
                    id=tag_id,
                )
                .one()
            )

            # Update the existing tag's attributes
            tag.value = tag_value if tag_value is not None else tag.value
            tag.creator_user_id = (
                creator_user_id
                if creator_user_id is not None
                else tag.creator_user_id
            )
            tag.type_id = (
                tag_type_id if tag_type_id is not None else tag.type_id
            )
            tag.active = (
                active_status if active_status is not None else tag.active
            )

        except NoResultFound:
            # If the tag doesn't exist, raise an error
            raise ValueError(
                f"Tag with id '{tag_id}' does not exist for fund_id '{fund_id}' and round_id '{round_id}'."
            )

        updated_tags.append(tag)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating tags: {str(e)}")
        raise ValueError(f"Error updating tags: {str(e)}")
    return updated_tags


def select_tags_for_fund_round(
    fund_id: str,
    round_id: str,
) -> List[Tag]:
    tags = (
        db.session.query(
            Tag.id,
            Tag.value,
            Tag.active,
            Tag.type_id,
            Tag.fund_id,
            Tag.round_id,
            Tag.creator_user_id,
            Tag.created_at,
            TagType.purpose.label("purpose"),
            TagType.description.label("description"),
        )
        .join(TagType, Tag.type_id == TagType.id)
        .filter(Tag.fund_id == fund_id)
        .filter(Tag.round_id == round_id)
        .all()
    )
    return tags


def select_tags_types() -> List[TagType]:
    return db.session.query(TagType).all()
