from db.models.assessment_record import AssessmentRecord
from db.models.score import Score
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from marshmallow.fields import Enum
from marshmallow.fields import Field
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy import auto_field


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    """AssessmentRecordMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = AssessmentRecord

    workflow_status = Enum(Status)
    language = Enum(Language)


class ScoreMetadata(SQLAlchemyAutoSchema):
    """ScoreMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = Score
        include_relationships = True
        load_instance = True
    
    application_id = auto_field(dump_only=True)

class AssessorTaskListMetadata(AssessmentRecordMetadata):
    """AssessorTaskListMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses.
    """

    short_id = auto_field(data_key="project_reference")
    date_submitted = Field(
        data_key="date_submitted", attribute="jsonb_blob.date_submitted"
    )

class AssessmentSubCriteriaMetadata(AssessmentRecordMetadata):
    """AssessmentSubCriteriaMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses.
    """

    funding_amount_requested=auto_field(data_key="funding_amount_requested")
    project_name=auto_field(data_key="project_name")
    fund_id=auto_field(data_key="fund_id")
    workflow_status=auto_field(data_key="workflow_status")
