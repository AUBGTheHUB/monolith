from __future__ import annotations

from typing import cast

import pytest
from fastapi import UploadFile

from src.exception import SponsorNotFoundError
from src.service.aws_service import AwsService
from src.service.image_service import ImageService
from tests.unit_tests.conftest import AwsServiceMock, ImageServiceMock

@pytest.fixture
def image_service(aws_service_mock: AwsServiceMock) -> ImageService:
    return ImageService(cast(AwsService, aws_service_mock))


@pytest.mark.asyncio
async def test_upload_image_success(
    image_service: ImageService, aws_service_mock: AwsServiceMock, image_mock: UploadFile
) -> None:
    aws_service_mock.upload_file.return_value = "https://somebucket.s3.some-place-1.amazonaws.com/somefile.webp"

    result = await sponsors_service.get_all()

    assert result.is_ok()
    assert result.unwrap() == sponsors
    sponsors_repo_mock.fetch_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_returns_ok(
    sponsors_service: SponsorsService,
    sponsors_repo_mock: SponsorsRepoMock,
    sponsor_mock: Sponsor,
) -> None:
    sponsors_repo_mock.fetch_by_id.return_value = Ok(sponsor_mock)

    result = await sponsors_service.get(str(sponsor_mock.id))

    assert result.is_ok()
    assert result.unwrap() == sponsor_mock
    sponsors_repo_mock.fetch_by_id.assert_awaited_once_with(str(sponsor_mock.id))
