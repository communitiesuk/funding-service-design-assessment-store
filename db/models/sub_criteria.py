import uuid
from itertools import chain

from db import db
from db.models.assessment import Assessment
from db.models.criteria import Criteria
from sqlalchemy_utils.types import UUIDType


class SubCriteria(db.Model):
    id = db.Column(
        "id",
        UUIDType(binary=False),
        default=uuid.uuid4,
        primary_key=True,
    )
    criteria_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey(Criteria.id),
    )
    sub_criteria_title = db.Column(
        db.Text(),
    )

    def __repr__(self):
        return f"<Sub-Criteria {self.sub_criteria_title}, {self.id} \
                for Criteria {self.criteria_id}>"

    def as_json(self):
        return {
            "id": str(self.id),
            "criteria_id": str(self.criteria_id),
            "sub_criteria_title": self.sub_criteria_title,
        }

    @property
    def uuid(self):
        return self.id


class SubCriteriaError(Exception):
    """Exception raised for errors in Sub-Criteria management

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Sorry, there was a problem, please try later"):
        self.message = message
        super().__init__(self.message)


class SubCriteriaMethods:
    @staticmethod
    def subcriterias_by_assessment_id(assessment_id: str, as_json=True):

        assessment_id = uuid.UUID(assessment_id)

        assessment = (
            db.session.query(Assessment)
            .filter(Assessment.id == assessment_id)
            .one()
        )
        fund_id = assessment.fund_id
        criterias_list = (
            db.session.query(Criteria)
            .filter(Criteria.fund_id == fund_id)
            .all()
        )
        criteria_ids_list = [str(criteria.id) for criteria in criterias_list]
        list_of_subcriteria_lists = [
            db.session.query(SubCriteria)
            .filter(SubCriteria.criteria_id == criteria_id)
            .all()
            for criteria_id in criteria_ids_list
        ]
        subcriteria_list = list(chain.from_iterable(list_of_subcriteria_lists))

        if as_json:
            return [subcriteria.as_json() for subcriteria in subcriteria_list]

        return subcriteria_list

    @staticmethod
    def get_by_id(id: str):
        subcriteria = db.session.get(SubCriteria, id)
        if subcriteria is None:
            raise SubCriteriaError(message="Sub-Criteria could not be found")

        return subcriteria
