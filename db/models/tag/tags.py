import uuid

from db import db
from db.models.tag.enums import Colour
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

BaseModel: DefaultMeta = db.Model


class Tag(BaseModel):
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )
    value = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    colour = db.Column(
        db.Enum(Colour, name="colour"), nullable=False, default=Colour.NONE
    )
    fund_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    round_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    creator = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now()
    )
    __table_args__ = (
        UniqueConstraint("value", "round_id", name="uq_tag_value_round_id"),
    )

    def __repr__(self):
        return f"<Tag {self.value}>"
