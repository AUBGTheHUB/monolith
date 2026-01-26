import boto3
from functools import lru_cache
from io import BytesIO
from os import environ

from botocore.exceptions import ClientError
from mypy_boto3_s3.client import S3Client
from structlog.stdlib import get_logger


LOG = get_logger()

AWS_S3_DEFAULT_BUCKET = environ["AWS_BUCKET"]

class AwsService:
    @lru_cache
    def get_s3_client(self) -> S3Client:
        return boto3.client("s3")

    def upload_file(self, file: BytesIO, file_name: str, content_type: str, bucket: str = AWS_S3_DEFAULT_BUCKET) -> None:

        client = self.get_s3_client()

        try:
            client.upload_fileobj(Fileobj=file, Bucket=bucket, Key=file_name, ExtraArgs={"ContentType": content_type})

        except ClientError as e:
            LOG.exception("There was an error with uploading the file ", error = e)
            raise e
