from db.models import Flag
from db.models.flags.enums import FlagType


flags = [
    Flag(
        justification="Test justification",
        section_to_flag="Test section",
        application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
        user_id="test-user-id",
        flag_type=FlagType.FLAGGED,
    ),
    Flag(
        justification="Test justification",
        section_to_flag="Test section",
        application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
        user_id="test-user-id",
        flag_type=FlagType.STOPPED,
    ),
    Flag(
        justification="Test justification",
        section_to_flag="Test section",
        application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
        user_id="test-user-id",
        flag_type=FlagType.RESOLVED,
    ),
    Flag(
        justification="Test justification",
        section_to_flag="Test section",
        application_id="a3ec41db-3eac-4220-90db-c92dea049c01",
        user_id="test-user-id",
        flag_type=FlagType.QA_COMPLETED,
    ),
]
