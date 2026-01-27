from __future__ import annotations

from pydantic import HttpUrl
import pytest

from src.exception import FileUploadError
from src.service.aws_service import AwsService
from tests.unit_tests.conftest import AwsServiceMock

from io import BytesIO


@pytest.fixture
def aws_service() -> AwsService:
    return AwsService()


@pytest.mark.asyncio
async def test_upload_file_success(aws_service: AwsService, aws_service_mock: AwsServiceMock) -> None:

    # Arrange
    file = BytesIO(b"some_file")
    file_name = "some_file.webp"
    content_type = "image/webp"
    bucket = "dabucket"
    region = "some-region-2"
    client = aws_service_mock.get_s3_client()

    # Act
    result = aws_service.upload_file(
        file=file, file_name=file_name, content_type=content_type, bucket=bucket, region=region, client=client
    )

    # Assert
    assert isinstance(result, HttpUrl)
    assert str(result) == f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}"


# @pytest.mark.asyncio
# async def test_upload_file_error_missing_file_name(aws_service: AwsService, aws_service_mock: AwsServiceMock) -> None:
#     file = BytesIO(b"some_file")
#     client = aws_service_mock.get_s3_client()

#     with pytest.raises(TypeError) as e:
#         aws_service.upload_file(file=file, client=client)


@pytest.mark.asyncio
async def test_upload_file_general_exception(aws_service: AwsService, aws_service_mock: AwsServiceMock) -> None:
    file = BytesIO(b"some_file")
    file_name = "some_file.webp"
    content_type = "image/webp"
    bucket = "dabucket"
    region = "some-region-2"
    client = aws_service_mock.get_s3_client()
    client.upload_fileobj.side_effect = Exception("Fake exception")

    with pytest.raises(FileUploadError) as e:
        aws_service.upload_file(
            file=file, file_name=file_name, content_type=content_type, bucket=bucket, region=region, client=client
        )
