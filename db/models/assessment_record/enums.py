from enum import Enum


# add APPLICATION_UPDATED here, it sits after NOT_STARTED and before IN_PROGRESS
# any move from NOT_STARTED OR IN_PROGRESS also counts from APPLICATION_UPDATED
# it shouldn't be valid from SUBMITTED or COMPLETED
class Status(Enum):
    """Status The ENUM used by `db.models.AssessmentRecord` to validate the
    possible values for the `workflow_status` column."""

    NOT_STARTED = 0
    IN_PROGRESS = 1
    SUBMITTED = 2
    COMPLETED = 3
    APPLICANT_UPDATED = 4


class Language(Enum):
    """Status The ENUM used by `db.models.AssessmentRecord` to validate the
    possible values for the `language` column."""

    en = 0
    cy = 1
