import time
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

import boto3
import pytest
from _helpers.context_aware_executor import ContextAwareExecutor
from _helpers.task_executer_service import TaskExecutorService
from config import Config
from moto import mock_aws
from sqlalchemy.exc import SQLAlchemyError
from tests.test_data.test_data_util import send_message_to_queue


class TestTaskExecutorService(unittest.TestCase):
    @mock_aws
    @pytest.mark.usefixtures("live_server")
    def test_message_in_mock_environment_processing_without_errors(self):
        self._mock_aws_client()
        self._add_data_to_queue()

        self.task_executor.process_messages()

        self._check_is_data_available(0)

    @mock_aws
    @pytest.mark.usefixtures("live_server")
    @patch("db.queries.assessment_records.queries.db.session.execute")
    def test_message_in_mock_environment_processing_with_errors(self, mocked_execute):
        self._mock_aws_client()
        self._add_data_to_queue()

        mocked_execute.side_effect = SQLAlchemyError("Error calling notification service")
        self.task_executor.process_messages()
        time.sleep(5)
        self._check_is_data_available(1)

    def _mock_aws_client(self):
        self.flask_app = MagicMock()
        self.executor = ContextAwareExecutor(max_workers=10, thread_name_prefix="NotifTask", flask_app=self.flask_app)
        self.task_executor = TaskExecutorService(flask_app=MagicMock(), executor=self.executor)
        s3_connection = boto3.client(
            "s3", region_name="us-east-1", aws_access_key_id="test_accesstoken", aws_secret_access_key="secret_key"
        )
        sqs_connection = boto3.client(
            "sqs", region_name="us-east-1", aws_access_key_id="test_accesstoken", aws_secret_access_key="secret_key"
        )
        s3_connection.create_bucket(Bucket=Config.AWS_MSG_BUCKET_NAME)
        self.queue_response = sqs_connection.create_queue(
            QueueName="import-queue.fifo", Attributes={"FifoQueue": "true"}
        )
        self.task_executor.sqs_extended_client.sqs_client = sqs_connection
        self.task_executor.sqs_extended_client.s3_client = s3_connection
        Config.AWS_SQS_IMPORT_APP_PRIMARY_QUEUE_URL = self.queue_response["QueueUrl"]

    def _add_data_to_queue(self):
        for x in range(1):
            application_attributes = {
                "application_id": {"StringValue": "8be9756e-8404-4d79-9b70-abf15066845f", "DataType": "String"},
                "S3Key": {
                    "StringValue": "assessment",
                    "DataType": "String",
                },
            }
            message_id = self.task_executor.sqs_extended_client.submit_single_message(
                queue_url=self.queue_response["QueueUrl"],
                message=send_message_to_queue,
                message_group_id="import_applications_group",
                message_deduplication_id=str(uuid4()),  # ensures message uniqueness
                extra_attributes=application_attributes,
            )
            assert message_id is not None

    def _check_is_data_available(self, count):
        response = self.task_executor.sqs_extended_client.receive_messages(
            queue_url=self.queue_response["QueueUrl"], max_number=1
        )
        assert len(response) == count
