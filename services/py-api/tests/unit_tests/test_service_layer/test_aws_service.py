from __future__ import annotations
from typing import Any, Generator

import boto3
from mypy_boto3_s3.client import S3Client
from pydantic import HttpUrl
import pytest
from pytest import MonkeyPatch
from moto import mock_aws

from src.exception import FileUploadError
from src.service.utility.aws_service import AwsService

from botocore.exceptions import ClientError

from io import BytesIO
from moto import mock_aws

from structlog.stdlib import get_logger

LOG = get_logger()


@pytest.fixture
def aws_client() -> Generator[Any, None, None]:
    """Provides a mocked S3 client."""
    with mock_aws():
        yield boto3.client("s3", region_name="eu-central-1")


@pytest.fixture
def aws_service(aws_client: S3Client) -> AwsService:
    """Provides an AwsService instance with a mocked client injected."""
    return AwsService(s3_client=aws_client)


@mock_aws
def test_ensure_bucket_exists_creates_when_no_bucket(aws_service: AwsService, monkeypatch: MonkeyPatch) -> None:
    bucket_name = "new-bucket"

    # Act
    aws_service.ensure_bucket_exists(bucket_name)

    # Assert - Verify the bucket actually exists in moto
    response = aws_service._s3_client.list_buckets()
    bucket_names = [b["Name"] for b in response["Buckets"]]
    assert bucket_name in bucket_names


@mock_aws
def test_ensure_bucket_exists_existing_bucket(aws_service: AwsService, monkeypatch: MonkeyPatch) -> None:
    bucket_name = "existing-bucket"
    # Pre-create the bucket
    aws_service._s3_client.create_bucket(
        Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "eu-central-1"}
    )

    # Setup a spy to ensure create_bucket isn't called again
    create_called = False
    original_create = aws_service._s3_client.create_bucket

    def spy_create_bucket(*args: Any, **kwargs: Any) -> Any:
        nonlocal create_called
        create_called = True
        return original_create(*args, **kwargs)

    monkeypatch.setattr(aws_service._s3_client, "create_bucket", spy_create_bucket)

    # Act
    aws_service.ensure_bucket_exists(bucket_name)

    # Assert
    assert create_called is False


@mock_aws
def test_upload_file_success(aws_service: AwsService) -> None:
    # Arrange
    aws_service.ensure_bucket_exists("dabucket")
    file = BytesIO(b"some_file")
    file_name = "some_file.webp"
    content_type = "image/webp"
    bucket = "dabucket"
    region = "eu-central-1"

    # Act
    result = aws_service.upload_file(
        file=file, file_name=file_name, content_type=content_type, bucket=bucket, region=region
    )

    # Assert
    assert isinstance(result, HttpUrl)
    assert str(result) == f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}"


@mock_aws
def test_upload_file_general_exception(aws_service: AwsService, monkeypatch: MonkeyPatch) -> None:
    file = BytesIO(b"some_file")

    # Trigger an error by patching the low-level upload method
    def raise_err(*args: Any, **kwargs: Any) -> Any:
        raise ClientError({"Error": {"Code": "500", "Message": "Injected Error"}}, "PutObject")

    monkeypatch.setattr(aws_service._s3_client, "upload_fileobj", raise_err)

    with pytest.raises(FileUploadError):
        aws_service.upload_file(file=file, file_name="test.png", content_type="image/png")


@mock_aws
def test_delete_file_success(aws_service: AwsService) -> None:
    bucket = "dabucket"
    file_name = "delete_me.webp"
    aws_service.ensure_bucket_exists(bucket)

    # Upload
    aws_service.upload_file(BytesIO(b"data"), file_name, "image/webp", bucket=bucket)

    # Delete
    aws_service.delete_file(file_name=file_name, bucket=bucket)

    # Assert 404
    with pytest.raises(ClientError) as exc:
        aws_service._s3_client.head_object(Bucket=bucket, Key=file_name)
    assert exc.value.response["Error"]["Code"] == "404"
