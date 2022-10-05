"""Flask Dev Pipeline Environment Configuration."""
from os import environ

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class DevConfig(DefaultConfig):

    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL").replace(
        "postgres://", "postgresql://"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
