from typing import Any
from io import BytesIO

from mypy_boto3_s3.client import S3Client
from pydantic import HttpUrl
from src.exception import FileUploadError, FileDeleteError
from src.service.utility.aws.environment import AWS_DEFAULT_REGION, AWS_S3_DEFAULT_BUCKET
from structlog.stdlib import get_logger
from botocore.exceptions import ClientError

LOG = get_logger()


class AwsService:

    def __init__(self, s3_client: S3Client) -> None:
        self._s3_client = s3_client

    def _ensure_bucket_exists(self, bucket: str = AWS_S3_DEFAULT_BUCKET) -> None:
        """A method to ensure that the bucket exists before calling any methods"""

        try:
            self._s3_client.head_bucket(Bucket=bucket)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code != "404":
                LOG.exception("There was an error when searching for the bucket", error=e)
                raise  # Handle other errors

            kwargs: dict[str, Any] = {
                "Bucket": bucket,
                "CreateBucketConfiguration": {"LocationConstraint": AWS_DEFAULT_REGION},
            }

            self._s3_client.create_bucket(**kwargs)

    def upload_file(
        self,
        file: BytesIO,
        file_name: str,
        content_type: str,
        bucket: str = AWS_S3_DEFAULT_BUCKET,
        region: str = AWS_DEFAULT_REGION,
    ) -> HttpUrl:
        """
        This method uploads the file to AWS and returns
        the address at which the file can be accessed.
        """

        try:
            self._s3_client.upload_fileobj(
                Fileobj=file, Bucket=bucket, Key=file_name, ExtraArgs={"ContentType": content_type}
            )
            return HttpUrl(url=f"https://{bucket}.s3.{region}.amazonaws.com/{file_name}")

        except Exception as e:
            LOG.exception("There was an error when uploading the file", error=e)
            raise FileUploadError() from e

    def delete_file(self, file_name: str, bucket: str = AWS_S3_DEFAULT_BUCKET) -> None:

        try:
            self._s3_client.delete_object(Bucket=bucket, Key=file_name)

        except Exception as e:
            LOG.exception("There was an error when deleting the file", error=e)
            raise FileDeleteError() from e
