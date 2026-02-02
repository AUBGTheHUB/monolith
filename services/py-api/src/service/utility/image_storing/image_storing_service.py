from PIL import Image
from io import BytesIO

from PIL.Image import Resampling
from fastapi import UploadFile

from pydantic import HttpUrl
from src.exception import ImageCompressionError, ImageDeleteError, ImageUploadError
from src.service.utility.aws.aws_service import AwsService
from src.service.utility.image_storing.constants import (
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_MAX_FILE_SIZE,
    DEFAULT_IMAGE_QUALITY,
)
from structlog.stdlib import get_logger

LOG = get_logger()


class ImageStoringService:
    def __init__(self, aws_service: AwsService) -> None:
        self._aws_service = aws_service

    def _compress_image(
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
            LOG.exception("There was an error when compressing the image", error=e)
            raise ImageCompressionError() from e

    async def upload_image(self, file: UploadFile, file_name: str) -> HttpUrl:
        """
        This method compresses the image,
        formats the file name so that the extension matches the file type,
        and uploads the image to the AWS S3 Bucket.
        The return value is the address at which the image can be accessed.
        """
        try:
            output = self._compress_image(file=await file.read())
            stripped_file_name = file_name[: file_name.rindex(".")]  # The file name without the extension
            formatted_file_name = (
                f"{stripped_file_name}.{DEFAULT_OUTPUT_FORMAT.lower()}"  # The file name with the extension
            )
            return self._aws_service.upload_file(
                file=output, file_name=formatted_file_name, content_type=f"image/{DEFAULT_OUTPUT_FORMAT.lower()}"
            )

        # A handler for when the file_name parameter doesn't have a file extension and is therefore invalid
        except ValueError as e:
            LOG.exception("There was an error when trimming the file name", error=e)
            raise ImageUploadError("The file name does not contain a file extension") from e

        # A handler for other unexpected exceptions
        except Exception as e:
            LOG.exception("There was an error when uploading the image", error=e)
            raise ImageUploadError() from e

    def delete_image(self, file_name: str) -> None:
        try:
            self._aws_service.delete_file(file_name)

        except Exception as e:
            LOG.exception("There was an error when deleting the image", error=e)
            raise ImageDeleteError() from e
