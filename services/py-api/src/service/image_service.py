from PIL import Image
from io import BytesIO
from os import environ

from PIL.Image import Resampling
from fastapi import UploadFile

from src.service.aws_service import AwsService

DEFAULT_MAX_FILE_SIZE: tuple = (2048, 2048)
DEFAULT_REGION: str = environ["AWS_DEFAULT_REGION"]
DEFAULT_IMAGE_QUALITY: int = 80 # Image quality relative to original file in %
DEFAULT_OUTPUT_FORMAT: str = "WEBP"

class ImageService:
    def __init__(self, aws_service: AwsService):
        self._aws_service = aws_service

    def upload_image(self, file: UploadFile, file_name: str) -> str:
        output = self.compress_image(file=file.read())
        stripped_file_name = file_name[:file_name.rindex(".")] # The file name without the extension
        self._aws_service.upload_file(file=output, file_name=f"{stripped_file_name}.{DEFAULT_OUTPUT_FORMAT.lower()}", content_type=f"image/{DEFAULT_OUTPUT_FORMAT.lower()}")
        return f"https://{bucket}.s3.{DEFAULT_REGION}.amazonaws.com/{str}"

    def compress_image(
        self,
        file: bytes, 
        max_file_size: tuple[float, float] = DEFAULT_MAX_FILE_SIZE,
        image_quality: int = DEFAULT_IMAGE_QUALITY, 
        output_format: str = DEFAULT_OUTPUT_FORMAT
    ) -> BytesIO:
        img = Image.open(BytesIO(file))
        img.thumbnail(max_file_size, Resampling.LANCZOS)

        output = BytesIO()

        img.save(
            fp=output,
            format=output_format,
            quality=image_quality,
            optimize=True
        )
        
        output.seek(0)
        return output