from db.models import Flag
from db.models.assessment_record import AssessmentRecord
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from db.models.comment import Comment
from db.models.comment.enums import CommentType
from db.models.flags.enums import FlagType
from db.models.score import Score
from marshmallow import fields
from marshmallow import Schema
from marshmallow.fields import Enum
from marshmallow.fields import Field
from marshmallow.fields import Method
from marshmallow.fields import Nested
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class AssessmentRecordMetadata(SQLAlchemyAutoSchema):
    """AssessmentRecordMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = AssessmentRecord

    def get_local_authority(self, obj):
        return obj.local_authority

    def get_funding_type(self, obj):
        return obj.funding_type

    def get_organisation_name(self, obj):
        return obj.organisation_name

    local_authority = Method("get_local_authority")
    funding_type = Method("get_funding_type")
    organisation_name = Method("get_organisation_name")

    workflow_status = Enum(Status)
    language = Enum(Language)
    flags = Nested(
        "FlagMetadata", many=True
    )  # TODO: Retrieve only latest flag


class ScoreMetadata(SQLAlchemyAutoSchema):
    """ScoreMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = Score
        include_relationships = True
        load_instance = True

    application_id = auto_field(dump_only=True)


class CommentMetadata(SQLAlchemyAutoSchema):
    """CommentMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True

    comment_type = Enum(CommentType)
    application_id = auto_field(dump_only=True)


class FlagMetadata(SQLAlchemyAutoSchema):
    """CommentMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses."""

    class Meta:
        model = Flag
        include_relationships = True
        load_instance = True

    flag_type = Enum(FlagType)
    application_id = auto_field(dump_only=True)


class AssessorTaskListMetadata(AssessmentRecordMetadata):
    """AssessorTaskListMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses.
    """

    short_id = auto_field(data_key="short_id")
    date_submitted = Field(
        data_key="date_submitted", attribute="jsonb_blob.date_submitted"
    )


class AssessmentSubCriteriaMetadata(AssessmentRecordMetadata):
    """AssessmentSubCriteriaMetadata The marshmallow class used to turn SQLAlchemy
    rows into json for return in http responses.
    """

    funding_amount_requested = auto_field(data_key="funding_amount_requested")
    project_name = auto_field(data_key="project_name")
    fund_id = auto_field(data_key="fund_id")
    workflow_status = Enum(Status)


class ProgressSchema(Schema):
    application_id = fields.Str()
    scored_sub_criterias = fields.Int()
