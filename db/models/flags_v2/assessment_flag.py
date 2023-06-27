from uuid import uuid4

from db import db
from db.models.flags_v2.flag_update import FlagStatus
from flask_sqlalchemy import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

BaseModel: DefaultMeta = db.Model


class AssessmentFlag(BaseModel):

    __tablename__ = "assessment_flag"

    id = Column("id", UUID(as_uuid=True), default=uuid4, primary_key=True)
    application_id = Column(
        "application_id",
        UUID(as_uuid=True),
        ForeignKey("assessment_records.application_id"),
    )
    latest_status = Column("latest_status", ENUM(FlagStatus))
    latest_allocation = Column("latest_allocation", String)
    sections_to_flag = db.Column(
        "sections_to_flag", ARRAY(db.String(256)), nullable=True
    )
    updates = relationship("FlagUpdate")
