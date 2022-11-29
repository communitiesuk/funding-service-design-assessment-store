from marshmallow.fields import Enum
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record.enums import Language, Status


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    """AssessmentRecordMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = AssessmentRecord
        exclude = ["jsonb_blob", "application_json_md5"]

    workflow_status = Enum(Status)
    language = Enum(Language)
