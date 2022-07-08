import uuid
from datetime import datetime

from db import db
from db.models.assessment import Assessment
from db.models.sub_criteria import SubCriteria
from sqlalchemy import DateTime
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils.types import UUIDType


class Comments(db.Model):
    comments_id = db.Column(
        "comments_id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    created_at = db.Column("created_at", DateTime(), default=datetime.utcnow())
    assessment_id = db.Column(
        "assessment_id",
        db.Text(),
        db.ForeignKey(Assessment.id),
    )
    person_id = db.Column(
        "person_id",
        db.Text(),
    )
    sub_criteria_id = db.Column(
        "sub_criteria_id",
        db.Text(),
        db.ForeignKey(SubCriteria.sub_criteria_id),
    )
    comment = db.Column(
        db.Text(),
    )

    def __repr__(self):
        return f"""Comments(
            assesment_id={self.assessment_id},
            person_id={self.person_id},
            sub_criteria_id={self.sub_criteria_id},
            comment={self.comment}
        )"""

    def __str__(self):
        return f"Comment {self.comment} \
                for Sub-Criteria {self.sub_criteria_id} \
                of Assessment {self.assessment_id} \
                by Person {self.person_id}>"

    def as_json(self):
        return {
            "scores_justifications_id": self.scores_justifications_id,
            "created_at": self.created_at,
            "assessment_id": self.assessment_id,
            "person_id": self.person_id,
            "sub_criteria_id": self.sub_criteria_id,
            "score": self.score,
            "justification": self.justification,
        }


class CommentsError(Exception):
    """Exception raised for errors in Comments management
    Attributes:
    message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class CommentsMethods:
    @staticmethod
    def comments(
        assessment_id: str, sub_criteria_id: str, person_id: str, comment: str
    ):
        try:
            newComment = Comments(
                assessment_id=assessment_id,
                sub_criteria_id=sub_criteria_id,
                person_id=person_id,
                comment=comment,
            )
            db.session.add(newComment)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise CommentsError()
        return newComment

    @staticmethod
    def comment(assessment_id: str, sub_criteria_id: str, as_json=False):
        comments = (
            db.session.query(Comments)
            .filter(
                Comments.assessment_id == assessment_id,
                Comments.sub_criteria_id == sub_criteria_id,
            )
            .all
        )
        if as_json:
            return [record.as_json() for record in comments]
        return comments
