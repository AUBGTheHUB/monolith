from __future__ import annotations
from typing import Any

from pydantic import HttpUrl
import pytest
from pytest import MonkeyPatch
from moto import mock_aws

from src.exception import FileUploadError
from src.service.utility.aws_service import AwsService

from botocore.exceptions import ClientError

from io import BytesIO
from os import environ
from moto import mock_aws

from structlog.stdlib import get_logger

LOG = get_logger()


@pytest.fixture(scope="session", autouse=True)
def generate_aws_data() -> None:
    """Mock AWS Credentials for testing moto."""
    environ["AWS_ACCESS_KEY_ID"] = "test-key"
    environ["AWS_SECRET_ACCESS_KEY"] = "test-key"
    environ["AWS_DEFAULT_REGION"] = "us-east-2"
    environ["AWS_S3_DEFAULT_BUCKET"] = "dabucket"


@pytest.fixture
def aws_service() -> AwsService:
    return AwsService()


@mock_aws
def test_ensure_bucket_exists_creates_when_no_bucket(aws_service: AwsService, monkeypatch: MonkeyPatch) -> None:
    s3_client = aws_service.get_s3_client()

    create_bucket_called = False

    # **kwargs is needed, since the create_bucket method has it as a parameter
    # and it is assigned a value in the code
    def call_create_bucket(**kwargs: dict[str, Any]) -> None:
        nonlocal create_bucket_called
        create_bucket_called = True

    monkeypatch.setattr(s3_client, "create_bucket", call_create_bucket)

    aws_service.ensure_bucket_exists("some_bucket")

    assert create_bucket_called is True


@mock_aws
def test_ensure_bucket_exists_existing_bucket(aws_service: AwsService, monkeypatch: MonkeyPatch) -> None:
    s3_client = aws_service.get_s3_client()

    create_bucket_called = True

    # **kwargs is needed, since the create_bucket method has it as a parameter
    # and it is assigned a value in the code
    def call_create_bucket(**kwargs: dict[str, Any]) -> None:
        nonlocal create_bucket_called
        create_bucket_called = False

    monkeypatch.setattr(s3_client, "create_bucket", call_create_bucket)

    aws_service.ensure_bucket_exists("dabucket")  # parameter is environ["AWS_S3_DEFAULT_BUCKET"]

    assert create_bucket_called is True


@mock_aws
def test_upload_file_success(aws_service: AwsService) -> None:

    # Arrange
    file = BytesIO(b"some_file")
    file_name = "some_file.webp"
    content_type = "image/webp"
    bucket = "dabucket"
    region = "us-east-2"

    # Act
    result = aws_service.upload_file(
        file=file, file_name=file_name, content_type=content_type, bucket=bucket, region=region
    )

    # Assert
    assert isinstance(result, HttpUrl)
    assert str(result) == f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}"


def test_upload_file_error_missing_file_name(aws_service: AwsService) -> None:

    file = BytesIO(b"some_file")
    content_type = "image/webp"

    with pytest.raises(ValueError) as e:
        aws_service.upload_file(file=file, file_name=None, content_type=content_type)


@mock_aws
def test_upload_file_general_exception(aws_service: AwsService, monkeypatch: MonkeyPatch) -> None:

    file = BytesIO(b"some_file")
    file_name = "some_file.webp"
    content_type = "image/webp"
    bucket = "dabucket"
    region = "us-east-2"
    s3_client = aws_service.get_s3_client()

    # Method to trigger a fake exception from the aws client
    def raise_exception() -> None:
        raise ClientError("Fake client error")

    monkeypatch.setattr(s3_client, "upload_fileobj", raise_exception)

    with pytest.raises(FileUploadError) as e:
        aws_service.upload_file(file=file, file_name=file_name, content_type=content_type, bucket=bucket, region=region)


@mock_aws
def test_delete_file_success(aws_service: AwsService) -> None:

    # Arrange
    file = BytesIO(b"some_file")
    file_name = "some_file.webp"
    content_type = "image/webp"
    bucket = "dabucket"
    region = "us-east-2"
    s3_client = aws_service.get_s3_client()

    # Upload file
    aws_service.upload_file(file=file, file_name=file_name, content_type=content_type, bucket=bucket, region=region)

    # Delete file
    aws_service.delete_file(file_name=file_name, bucket=bucket)

    # Assert
    with pytest.raises(ClientError) as err:
        s3_client.head_object(Bucket=bucket, Key=file_name)

    error_code = err.value.response["Error"]["Code"]
    assert error_code == "404"
