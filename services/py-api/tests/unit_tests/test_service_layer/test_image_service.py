from __future__ import annotations

from typing import cast

from pydantic import HttpUrl
import pytest
from fastapi import UploadFile

from src.exception import ImageCompressionError
from src.service.aws_service import AwsService
from src.service.image_service import ImageService
from tests.unit_tests.conftest import AwsServiceMock

from io import BytesIO
from PIL import Image


@pytest.fixture
def image_service(aws_service_mock: AwsServiceMock) -> ImageService:
    return ImageService(cast(AwsService, aws_service_mock))


@pytest.fixture
def image_data_mock() -> bytes:
    image = Image.new("RGB", (2000, 1600), color="red")
    output = BytesIO()
    image.save(fp=output, format="JPEG")
    output.seek(0)
    return output.getvalue()


@pytest.fixture
def image_name_mock() -> str:
    return "my_image.jpg"


@pytest.fixture
def image_mock() -> UploadFile:
    image = Image.new("RGB", (2000, 1600), color="red")
    output = BytesIO()
    image.save(fp=output, format="JPEG")
    output.seek(0)
    return UploadFile(filename="my_image.jpg", file=output)


@pytest.mark.asyncio
async def test_upload_image_success(
    image_service: ImageService, aws_service_mock: AwsServiceMock, image_mock: UploadFile, image_name_mock: str
) -> None:
    formatted_image_name_mock = image_name_mock[: image_name_mock.rindex(".")]
    aws_service_mock.upload_file.return_value = HttpUrl(
        f"https://somebucket.s3.some-place-1.amazonaws.com/{formatted_image_name_mock}.webp"
    )

    result = await image_service.upload_image(image_mock, image_name_mock)

    assert isinstance(result, HttpUrl)
    assert str(result) == f"https://somebucket.s3.some-place-1.amazonaws.com/{formatted_image_name_mock}.webp"


@pytest.mark.asyncio
async def test_compress_image_returns_bytesio(image_service: ImageService, image_data_mock: bytes) -> None:
    output = image_service.compress_image(image_data_mock)

    assert isinstance(output, BytesIO)
    assert output.tell() == 0  # Check if the pointer is at the start of the buffer


@pytest.mark.asyncio
async def test_compress_image_produces_valid_image(image_service: ImageService, image_data_mock: bytes) -> None:
    output = image_service.compress_image(image_data_mock)

    image = Image.open(output)
    image.verify()  # Check if image is corrupted


@pytest.mark.asyncio
async def test_compress_image_size_constraints(image_service: ImageService, image_data_mock: bytes) -> None:
    max_size: tuple[float, float] = (1024, 1024)
    output = image_service.compress_image(file=image_data_mock, max_file_size=max_size)

    image = Image.open(output)
    assert image.width <= max_size[0]
    assert image.width <= max_size[1]


@pytest.mark.asyncio
async def test_compress_image_format(image_service: ImageService, image_data_mock: bytes) -> None:
    output = image_service.compress_image(file=image_data_mock, output_format="WEBP")

    image = Image.open(output)
    assert image.format == "WEBP"


@pytest.mark.asyncio
async def test_compress_image_compression(image_service: ImageService, image_data_mock: bytes) -> None:
    output = image_service.compress_image(file=image_data_mock, image_quality=30)

    Image.open(output)
    assert len(output.getvalue()) < len(image_data_mock)


@pytest.mark.asyncio
async def test_compress_error(image_service: ImageService) -> None:
    with pytest.raises(ImageCompressionError) as e:
        image_service.compress_image(file=b"some_fake_image")
