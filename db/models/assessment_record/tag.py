from db import db
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

BaseModel: DefaultMeta = db.Model


class Tag(BaseModel):

    __tablename__ = "tag"

    application_id = Column(
        "application_id",
        UUID(as_uuid=True),
        ForeignKey(
            "assessment_records.application_id",
        ),
        primary_key=True,
    )
    tag_value = Column("tag_value", String, nullable=False, primary_key=True)
