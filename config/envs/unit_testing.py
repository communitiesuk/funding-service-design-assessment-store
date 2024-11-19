"""Flask Unit Testing Environment Configuration."""
from config.envs.default import DefaultConfig
from config.mappings.assessment_mapping_fund_round import (
    fund_round_data_key_mappings,
)
from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class UnitTestingConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = CommonConfig.SESSION_COOKIE_NAME
    FLASK_ENV = "unit_test"

    # APIs
    APPLICATION_STORE_API_HOST = CommonConfig.TEST_APPLICATION_STORE_API_HOST
    ACCOUNT_STORE_API_HOST = CommonConfig.TEST_ACCOUNT_STORE_API_HOST

    # Security
    FORCE_HTTPS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WARN_IF_QUERIES_OVER_MS = 5

    SQLALCHEMY_DATABASE_URI = DefaultConfig.SQLALCHEMY_DATABASE_URI + "_UNIT_TEST"

    # ---------------
    # Task Executor Config
    # ---------------
    TASK_EXECUTOR_MAX_THREAD = 5  # max amount of threads
    # ---------------
    # S3 Config
    # ---------------
    AWS_MSG_BUCKET_NAME = "fsd-notification-bucket"

    AWS_SQS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID = "test_access_id"
    AWS_SQS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY = "test_secret_key"  # pragma: allowlist secret
    AWS_SQS_REGION = AWS_REGION = "eu-west-2"
    AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = "test_primary_url"
    AWS_SQS_IMPORT_APP_SECONDARY_QUEUE_URL = "test_secondary_url"

    # ---------------
    # SQS Config
    # ---------------
    SQS_WAIT_TIME = 2  # max time to wait (in sec) before returning
    SQS_BATCH_SIZE = 10  # MaxNumber Of Messages to process
    SQS_VISIBILITY_TIME = 1  # time for message to temporarily invisible to others (in sec)
    SQS_RECEIVE_MESSAGE_CYCLE_TIME = 5  # Run the job every 'x' seconds

    fund_round_data_key_mappings.update(
        {
            "TESTREF": {
                "location": "yEmHpp",
                "asset_type": "yaQoxU",
                "funding_one": "JzWvhj",
                "funding_two": "jLIgoi",
            }
        }
    )

    DATA_KEY_MAPPING_CONFIG = fund_round_data_key_mappings
