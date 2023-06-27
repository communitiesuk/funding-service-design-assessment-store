"""The module containing all code related to the `assessment_records` table
within the Postgres db.

Tangential structures such as triggers and ENUMS are kept in other
files.
"""
from db import db
from db.models.assessment_record.enums import Language
from db.models.assessment_record.enums import Status
from flask_sqlalchemy import DefaultMeta
from sqlalchemy import cast
from sqlalchemy import Column
from sqlalchemy import Computed
from sqlalchemy import func
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property
from sqlalchemy.orm import relationship

BaseModel: DefaultMeta = db.Model


class AssessmentRecord(BaseModel):
    """AssessmentRecord The sqlalchemy-flask model class used to define the
    `assessment_records` table in the Postgres database."""

    __tablename__ = "assessment_records"

    application_id = Column("application_id", UUID, primary_key=True)

    short_id = Column("short_id", db.String(255), nullable=False)

    type_of_application = Column(
        "type_of_application", db.String(255), index=True, nullable=False
    )

    project_name = Column(
        "project_name", db.String(255), index=True, nullable=False
    )

    funding_amount_requested = Column(
        "funding_amount_requested", db.Float(), index=True, nullable=False
    )

    round_id = Column("round_id", UUID, index=True, nullable=False)

    fund_id = Column("fund_id", UUID, index=True, nullable=False)

    language = Column("language", ENUM(Language), default="en")

    workflow_status = Column(
        "workflow_status", ENUM(Status), index=True, default="NOT_STARTED"
    )

    asset_type = Column(
        "asset_type", db.String(255), index=True, nullable=False
    )

    jsonb_blob = Column("jsonb_blob", JSONB, nullable=False)

    application_json_md5 = Column(
        "application_json_md5",
        TEXT,
        Computed(func.md5(cast(jsonb_blob, TEXT)), persisted=True),
    )

    scores = relationship("Score")

    comments = relationship("Comment")

    flags = relationship("Flag")
    flags_v2 = relationship("AssessmentFlag")

    location_json_blob = Column("location_json_blob", JSONB, nullable=True)

    # These are defined as column_properties not as hybrid_property due to performance
    # Using column_property below forces the json parsing to be done on the DB side which is quicker than in python
    organisation_name = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "opFJRm").answer',
        )
    )
    local_authority = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "nURkuc").answer',
        )
    )
    funding_type = column_property(
        func.jsonb_path_query_first(
            jsonb_blob,
            '$.forms[*].questions[*].fields[*] ? (@.key == "NxVqXd").answer',
        )
    )


Index(
    "ix_application_jsonb",
    AssessmentRecord.jsonb_blob,
    postgresql_ops={
        "jsonb_blob": "jsonb_path_ops",
    },
    postgresql_using="gin",
)

# This is very fast for "=" in WHERE clauses.
Index(
    "ix_application_id_hash",
    AssessmentRecord.application_id,
    postgresql_using="hash",
)

# Links the round_id and fund_id columns by an index.
Index(
    "ix_application_round_fund_id",
    AssessmentRecord.round_id,
    AssessmentRecord.fund_id,
)

Index(
    "ix_project_name",
    AssessmentRecord.project_name,
    postgresql_ops={
        "project_name": "gin_trgm_ops",
    },
    postgresql_using="gin",
)
