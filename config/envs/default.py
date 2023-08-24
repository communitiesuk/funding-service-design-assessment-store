"""Flask configuration."""
from os import environ
from pathlib import Path

from config.mappings.assessment_mapping_fund_round import (
    fund_round_to_assessment_mapping,
)
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class DefaultConfig:

    # ---------------
    #  General App Config
    # ---------------

    SECRET_KEY = CommonConfig.SECRET_KEY
    SESSION_COOKIE_NAME = CommonConfig.SESSION_COOKIE_NAME
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)
    FLASK_ENV = CommonConfig.FLASK_ENV
    FORCE_HTTPS = CommonConfig.FORCE_HTTPS
    FSD_LOG_LEVEL = CommonConfig.FSD_LOG_LEVEL

    # ---------------
    # APIs Config: contains api hosts (set in manifest.yml)
    # ---------------

    # Application Store
    APPLICATION_STORE_API_HOST = CommonConfig.APPLICATION_STORE_API_HOST
    APPLICATIONS_ENDPOINT = CommonConfig.APPLICATIONS_ENDPOINT
    APPLICATION_ENDPOINT = CommonConfig.APPLICATION_ENDPOINT

    # ---------------
    # Database
    # ---------------

    SQLALCHEMY_DATABASE_URI = environ["DATABASE_URL"].replace(
        "postgres://", "postgresql://"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ASSESSMENT_MAPPING_CONFIG = fund_round_to_assessment_mapping

    # ---------------
    # SQS Config
    # ---------------
    SQS_WAIT_TIME = 0  # max time to wait (in sec) before returning
    SQS_BATCH_SIZE = 1  # MaxNumber Of Messages to process
    SQS_VISIBILITY_TIME = (
        0  # time for message to temporarily invisible to others (in sec)
    )
    SQS_RECEIVE_MESSAGE_CYCLE_TIME = 60  # Run the job every 'x' seconds
