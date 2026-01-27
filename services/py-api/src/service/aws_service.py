import boto3
from functools import lru_cache
from io import BytesIO
from os import environ

from mypy_boto3_s3.client import S3Client
from pydantic import HttpUrl
from src.exception import FileUploadError
from structlog.stdlib import get_logger


LOG = get_logger()

AWS_S3_DEFAULT_BUCKET = environ["AWS_BUCKET"]
AWS_DEFAULT_REGION: str = environ["AWS_DEFAULT_REGION"]


class AwsService:
    @lru_cache
    def get_s3_client(self) -> S3Client:
        return boto3.client("s3")

    """
    This method uploads the file to AWS and returns
    the address at which the file can be accessed.
    """

    def upload_file(
        self,
        file: BytesIO,
        file_name: str,
        content_type: str,
        bucket: str = AWS_S3_DEFAULT_BUCKET,
        region: str = AWS_DEFAULT_REGION,
        client: S3Client | None = None,
    ) -> HttpUrl:

        if client is None:
            client = self.get_s3_client()

        try:
            client.upload_fileobj(Fileobj=file, Bucket=bucket, Key=file_name, ExtraArgs={"ContentType": content_type})
            return HttpUrl(url=f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}")

        except Exception as e:
            LOG.exception("There was an error when uploading the file", error=e)
            raise FileUploadError() from e
