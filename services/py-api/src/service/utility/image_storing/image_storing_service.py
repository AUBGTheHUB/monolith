from PIL import Image
from io import BytesIO

from PIL.Image import Resampling
from fastapi import UploadFile

from pydantic import HttpUrl
from src.exception import ImageCompressionError, ImageDeleteError, ImageUploadError
from src.service.utility.aws_service import AwsService
from src.service.utility.image_storing.constants import (
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_MAX_FILE_SIZE,
    DEFAULT_IMAGE_QUALITY,
)


class ImageStoringService:
    def __init__(self, aws_service: AwsService) -> None:
        self._aws_service = aws_service

    """
    This method compresses the image,
    formats the file name so that the extension matches the file type,
    and uploads the image to the AWS S3 Bucket.
    The return value is the address at which the image can be accessed.
    """

    async def upload_image(self, file: UploadFile, file_name: str) -> HttpUrl:
        try:
            output = self.compress_image(file=await file.read())
            stripped_file_name = file_name[: file_name.rindex(".")]  # The file name without the extension
            formatted_file_name = (
                f"{stripped_file_name}.{DEFAULT_OUTPUT_FORMAT.lower()}"  # The file name with the extension
            )
            return self._aws_service.upload_file(
                file=output, file_name=formatted_file_name, content_type=f"image/{DEFAULT_OUTPUT_FORMAT.lower()}"
            )

        # This exception is usually ClientError -
        # e.g. when file_name doesn't have an extension and therefore cannot be trimmed
        except Exception as e:
            raise ImageUploadError() from e

    def delete_image(self, file_name: str) -> None:
        try:
            self._aws_service.delete_file(file_name)

        except Exception as e:
            raise ImageDeleteError() from e

    def compress_image(
        self,
        file: bytes,
        max_file_size: tuple[float, float] = DEFAULT_MAX_FILE_SIZE,
        image_quality: int = DEFAULT_IMAGE_QUALITY,
        output_format: str = DEFAULT_OUTPUT_FORMAT,
    ) -> BytesIO:
        try:
            img = Image.open(BytesIO(file))
            img.thumbnail(max_file_size, Resampling.LANCZOS)

            output = BytesIO()

            img.save(fp=output, format=output_format, quality=image_quality, optimize=True)

            output.seek(0)  # Return reader to the start of the file
            return output

        except Exception as e:
            raise ImageCompressionError() from e
