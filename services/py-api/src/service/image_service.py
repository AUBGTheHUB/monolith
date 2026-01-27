from PIL import Image
from io import BytesIO

from PIL.Image import Resampling
from fastapi import UploadFile

from pydantic import HttpUrl
from src.exception import ImageCompressionError
from src.service.aws_service import AwsService

DEFAULT_MAX_FILE_SIZE: tuple[float, float] = (2048, 2048)
DEFAULT_IMAGE_QUALITY: int = 80  # Image quality relative to original file in %
DEFAULT_OUTPUT_FORMAT: str = "WEBP"


class ImageService:
    def __init__(self, aws_service: AwsService):
        self._aws_service = aws_service

    """
    This method compresses the image,
    formats the file name so that the extension matches the file type,
    and uploads the image to the AWS S3 Bucket.
    The return value is the address at which the image can be accessed.
    """

    async def upload_image(self, file: UploadFile, file_name: str) -> HttpUrl:
        output = self.compress_image(file=await file.read())
        stripped_file_name = file_name[: file_name.rindex(".")]  # The file name without the extension
        formatted_file_name = (
            f"{stripped_file_name}.{DEFAULT_OUTPUT_FORMAT.lower()}"  # The file name with the extension
        )
        return self._aws_service.upload_file(
            file=output, file_name=formatted_file_name, content_type=f"image/{DEFAULT_OUTPUT_FORMAT.lower()}"
        )

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
