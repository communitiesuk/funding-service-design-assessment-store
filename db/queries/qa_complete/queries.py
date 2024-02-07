"""Queries which are performed on the `flags` table.

Joins allowed.

"""
from typing import Dict

from db import db
from db.models.qa_complete.qa_complete import QaComplete
from db.schemas.schemas import QaCompleteMetadata


def create_qa_complete_record(
    application_id: str,
    user_id: str,
) -> Dict:
    qa_complete_record = QaComplete(
        application_id=application_id,
        user_id=user_id,
    )
    db.session.add(qa_complete_record)
    db.session.commit()

    metadata_serialiser = QaCompleteMetadata()
    flag_metadata = metadata_serialiser.dump(qa_complete_record)

    return flag_metadata


def get_qa_complete_record_for_application(application_id) -> Dict:
    qa_complete_record_for_application = QaComplete.query.filter(QaComplete.application_id == application_id).all()
    metadata_serialiser = QaCompleteMetadata()
    qa_complete_metadata = metadata_serialiser.dump(
        qa_complete_record_for_application[0] if qa_complete_record_for_application else []
    )
    return qa_complete_metadata
