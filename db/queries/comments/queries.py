"""Queries which are performed on the `scores` table.

Joins allowed.

"""
from collections import defaultdict
from typing import Dict

from db import db
from db.models.comment.comments import Comment
from db.models.comment.comments_update import CommentsUpdate
from db.models.comment.enums import CommentType
from db.schemas import CommentMetadata
from sqlalchemy import and_
from sqlalchemy import select


def get_comments_from_db(
    application_id: str = None,
    sub_criteria_id: str = None,
    theme_id: str = None,
    comment_id: str = None,
    comment_type: CommentType = None,
) -> list[dict]:
    """Retrieve comments based on provided criteria.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param theme_id: Optional theme_id, if not supplied returns all
        comments for subcriteria.
    :param comment_id: The stringified comment UUID.
    :return: List of dictionaries representing comments.

    """
    # Create a base query to retrieve Comment objects ordered by date_created
    query = db.session.query(Comment).order_by(Comment.date_created.desc())
    filters = []

    if comment_id:
        # Filter the query to retrieve only the comment with the given comment_id
        filters.append(Comment.id == comment_id)
    elif application_id:
        filters.append(Comment.application_id == application_id)
        if sub_criteria_id:
            filters.append(Comment.sub_criteria_id == sub_criteria_id)
        if theme_id:
            filters.append(Comment.theme_id == theme_id)

    if comment_type:
        filters.append(Comment.comment_type == comment_type)

    # Combine multiple filters using logical AND using the `and_` function from SQLAlchemy
    query = query.filter(and_(*filters))

    comment_rows = query.all()
    metadata_serializer = CommentMetadata()
    comment_metadatas = [metadata_serializer.dump(comment_row) for comment_row in comment_rows]

    return comment_metadatas


def create_comment(
    application_id: str,
    sub_criteria_id: str,
    comment: str,
    comment_type: str,
    user_id: str,
    theme_id: str,
) -> Dict:
    """create_comment_for_application_sub_crit executes a query on comments which
    creates a comment for the given application_id and sub_criteria_id.

    :param application_id: The stringified application UUID.
    :param sub_criteria_id: The stringified sub_criteria UUID.
    :param comment: The comment string.
    :param comment_type: The type of comment for ENUM.
    :param date_created: The date_created.
    :param user_id: The stringified user_id.
    :return: dictionary.

    """
    comment_update = CommentsUpdate(comment=comment)

    comment = Comment(
        application_id=application_id,
        sub_criteria_id=sub_criteria_id,
        comment_type=comment_type,
        user_id=user_id,
        theme_id=theme_id,
        updates=[comment_update],
    )
    db.session.add(comment)
    db.session.commit()
    metadata_serialiser = CommentMetadata()
    comment_metadata = metadata_serialiser.dump(comment)

    return comment_metadata


def update_comment(
    comment: str,
    comment_id: str,
) -> Dict:
    """update_comment executes a query on comments which updates a comment for the
    given comment id.

    :param comment: The comment string.
    :param comment_id: The comment id.
    :return: dictionary.

    """
    stmt = select(Comment).where(Comment.id == comment_id)
    comment_to_update = db.session.scalars(stmt).one()

    comment_update = CommentsUpdate(comment_id=comment_id, comment=comment)
    comment_to_update.updates.append(comment_update)

    db.session.add(comment_to_update)
    db.session.commit()
    metadata_serialiser = CommentMetadata()
    comment_metadata = metadata_serialiser.dump(comment_to_update)

    return comment_metadata


def get_sub_criteria_to_has_comment_map(application_id: str) -> dict:
    stmt = (
        select(Comment.sub_criteria_id).select_from(Comment).where(Comment.application_id == application_id).distinct()
    )

    result = db.session.execute(stmt).fetchall()

    sub_criteria_to_has_comment_map = defaultdict(lambda: False)
    for (sub_criteria_id,) in result:
        sub_criteria_to_has_comment_map[sub_criteria_id] = True

    return sub_criteria_to_has_comment_map
