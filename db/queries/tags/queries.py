from typing import List

from db import db
from db.models.tag.tags import Tag
from flask import current_app
from sqlalchemy.dialects.postgresql import insert as postgres_insert


def insert_tags(tags, fund_id, round_id):
    """
    Inserts tags associated with a round.

    Args:
        tags (list): A list of tag dictionaries [{
                "value": "",
                "colour": "",
                "user": "",
            }]
        round_id (str): The round to insert tags for.
        fund_id (str): The fund to insert tags for.

    Returns:
        inserted_tags (list): This method returns a list of inserted tags (the tag id and key)
    """
    stmt = postgres_insert(Tag).returning(Tag)
    values = [
        {
            "value": tag["value"],
            "fund_id": fund_id,
            "round_id": round_id,
            "creator": tag["user"],
            "colour": tag.get("colour", "NONE"),
        }
        for tag in tags
    ]

    result = db.session.execute(stmt.values(values))
    inserted_rows = result.fetchall()
    inserted_tag_values = [row.value for row in inserted_rows]
    db.session.commit()
    current_app.logger.info(f"Inserted tags: {inserted_tag_values}.")

    return inserted_rows


def select_tags_for_fund_round(
    fund_id: str,
    round_id: str,
) -> List[Tag]:
    tags = (
        db.session.query(Tag)
        .where(Tag.fund_id == fund_id)
        .where(Tag.round_id == round_id)
    ).all()
    return tags
