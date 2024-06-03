from os import getenv

import connexion
from _helpers.context_aware_executor import ContextAwareExecutor
from _helpers.scheduler_service import scheduler_executor
from _helpers.task_executer_service import TaskExecutorService
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from connexion.resolver import MethodViewResolver
from flask import Flask
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import DbChecker
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from fsd_utils.services.aws_extended_client import SQSExtendedClient
from openapi.utils import get_bundled_specs


def create_app() -> Flask:
    init_sentry()
    connexion_options = {
        "swagger_url": "/",
    }
    connexion_app = connexion.FlaskApp(__name__, specification_dir="openapi/", options=connexion_options)
    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        validate_responses=True,
        resolver=MethodViewResolver("api"),
    )

    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")
    flask_app.json.sort_keys = False

    # Initialise logging
    logging.init_app(flask_app)

    # Initialize sqs extended client
    create_sqs_extended_client(flask_app)

    from db import db, migrate

    # Bind SQLAlchemy ORM to Flask app
    db.init_app(flask_app)
    # Bind Flask-Migrate db utilities to Flask app
    migrate.init_app(
        flask_app,
        db,
        directory="db/migrations",
        render_as_batch=True,
        compare_type=True,
        compare_server_default=True,
    )

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())
    health.add_check(DbChecker(db))

    executor = ContextAwareExecutor(
        max_workers=Config.TASK_EXECUTOR_MAX_THREAD, thread_name_prefix="NotifTask", flask_app=flask_app
    )
    # Configure Task Executor service
    task_executor_service = TaskExecutorService(flask_app=flask_app, executor=executor)
    # Configurations for Flask-Apscheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=scheduler_executor,
        trigger="interval",
        seconds=flask_app.config["SQS_RECEIVE_MESSAGE_CYCLE_TIME"],  # Run the job every 'x' seconds
        kwargs={"task_executor_service": task_executor_service},
    )
    scheduler.start()

    try:
        # To keep the main thread alive (scheduler to run only on main thread)
        return flask_app
    except Exception:
        # shutdown if execption occurs when returning app
        return scheduler.shutdown()


def create_sqs_extended_client(flask_app):
    if (
        getenv("AWS_ACCESS_KEY_ID", "Access Key Not Available") == "Access Key Not Available"
        and getenv("AWS_SECRET_ACCESS_KEY", "Secret Key Not Available") == "Secret Key Not Available"
    ):
        flask_app.extensions["sqs_extended_client"] = SQSExtendedClient(
            region_name=Config.AWS_REGION,
            endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
            large_payload_support=Config.AWS_MSG_BUCKET_NAME,
            always_through_s3=True,
            delete_payload_from_s3=True,
            logger=flask_app.logger,
        )
    else:
        flask_app.extensions["sqs_extended_client"] = SQSExtendedClient(
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION,
            endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
            large_payload_support=Config.AWS_MSG_BUCKET_NAME,
            always_through_s3=True,
            delete_payload_from_s3=True,
            logger=flask_app.logger,
        )


app = create_app()
