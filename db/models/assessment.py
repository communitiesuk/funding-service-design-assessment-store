import uuid

from db import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy_utils.types import UUIDType


class Assessment(db.Model):
    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    compliance_status = db.Column(db.Text(), default="UNASSESSED")
    application_id = db.Column(db.Text(), index=True, unique=True)

    def __repr__(self):
        return f"<Assessment {self.id} for Application {self.application_id}>"

    def as_json(self):
        return {
            "id": self.id,
            "compliance_status": self.compliance_status,
            "applicationId": self.application_id,
        }


class AssessmentError(Exception):
    """Exception raised for errors in Assessment management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class AssessmentMethods:
    @staticmethod
    def assessments(as_json=False):
        assessments = Assessment.query.all()
        if as_json:
            return [assessment.as_json() for assessment in assessments]
        return assessments

    @staticmethod
    def get_by_id(assessment_id: str):
        assessment = Assessment.query.get(assessment_id)
        if not assessment:
            raise AssessmentError(message="Assessment could not be found")
        return assessment

    @staticmethod
    def register_application(application_id: str):
        try:
            assessment = Assessment(application_id=application_id)
            db.session.add(assessment)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise AssessmentError(
                message="An assessment for this application already exists"
            )
        return assessment

    @staticmethod
    def update_status(assessment_id: str, status: str):
        """Function searches for an assessment_id from database
        & updates the compliance status to new status.

        Args:
            assessment_id (str): assessment_id.
            status (str): compliance_status.

        Returns:
            class object with updated status, assessment id
            and application id.
        """
        assessment_id = AssessmentMethods.get_by_id(assessment_id)
        assessment_id.compliance_status = status
        db.session.commit()
        return Assessment(
            application_id=assessment_id.application_id,
            id=assessment_id.id,
            compliance_status=assessment_id.compliance_status,
        )

    @staticmethod
    def add_comment(assessment_id: str, comment: str):
        """Function searches for an assessment_id from database
        & adds a comment.

        Args:
            assessment_id (str): assessment_id.
            status (str): compliance_status.

        Returns:
            class object with updated status, assessment id
            and application id.
        """
        return ""
