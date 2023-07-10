import re
import uuid

from db import db
from db.models.tag.enums import Colour
from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy import Column
from sqlalchemy import func
from sqlalchemy import Index
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.event import listens_for
from sqlalchemy.orm import validates

BaseModel: DefaultMeta = db.Model


class Tag(BaseModel):
    __tablename__ = "tag"
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )
    value = Column(
        db.String(255),
        nullable=False,
        unique=False,
    )
    active = Column(db.Boolean(), nullable=False, default=True)
    colour = Column(
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
    creator_user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
    )
    created_at = Column(db.DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        Index(
            "tag_value_round_id_ix",
            text("lower(value)"),
            "round_id",
            unique=True,
        ),
    )

    def __repr__(self):
        return f"<Tag {self.value}>"

    @validates("value")
    def validate_value(self, key, value):
        # Remove leading and trailing whitespace
        value = value.strip()

        # Define the pattern using a regular expression
        pattern = r"^[\'\-\w\s]+$"

        # Check if the value matches the pattern
        if not re.match(pattern, value):
            raise ValueError(
                "Invalid value. The value should only contain apostrophes, hyphens, letters, digits, and spaces."
            )

        return value


@listens_for(Tag, "before_insert")
@listens_for(Tag, "before_update")
def validate_tag(mapper, connection, target):
    # Trigger attribute-level validation only for the 'value' column
    value = target.value
    target.validate_value("value", value)
