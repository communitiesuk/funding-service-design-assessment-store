from db import db
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID


BaseModel: DefaultMeta = db.Model


class AllocationAssociation(BaseModel):
    __tablename__ = "allocation_association"
    application_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "assessment_records.application_id",
        ),
        nullable=False,
    )
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    active = db.Column(db.Boolean(), nullable=False, default=True)
    log = db.Column(JSONB, nullable=False)
    __table_args__ = (db.PrimaryKeyConstraint("application_id", "user_id"),)
