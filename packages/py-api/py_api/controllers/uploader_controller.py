from os import getenv, path
from shutil import copyfileobj
from tempfile import gettempdir
from typing import Any, Dict

import boto3
from fastapi import UploadFile


class UploaderController:
    _AWS_PUB_KEY = getenv("AWS_PUB_KEY", "")
    _AWS_PRIV_KEY = getenv("AWS_PRIV_KEY", "")
    _AWS_BUCKET_NAME = getenv("AWS_BUCKET_NAME", "")

    _s3_client = boto3.client(
        's3',
        aws_access_key_id=_AWS_PUB_KEY,
        aws_secret_access_key=_AWS_PRIV_KEY,
    )

    _s3_resource = boto3.resource(
        's3',
        aws_access_key_id=_AWS_PUB_KEY,
        aws_secret_access_key=_AWS_PRIV_KEY,
    )

    @classmethod
    def _get_url_of_object(cls, location: str, bucket_name: str, url_name: str) -> str:
        return "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, url_name)

    @classmethod
    def upload_object(cls, file: UploadFile, file_name: str) -> Dict[str, Any]:
        s3 = cls._s3_client

        # TODO: Schedule more frequent temp dir cleanups on the server
        tmpdir = gettempdir()
        with open(path.join(tmpdir, file.filename), "wb+") as file_object:
            copyfileobj(file.file, file_object)

        saved_file = file_name + "." + file.filename.rsplit('.')[1]

        s3.upload_file(
            f'{tmpdir}/{file.filename}',
            cls._AWS_BUCKET_NAME, saved_file, ExtraArgs={
                'ContentType': 'image/jpeg',
            },
        )

        location = s3.get_bucket_location(Bucket=cls._AWS_BUCKET_NAME)[
            'LocationConstraint'
        ]

        return {
            "message": "Upload was successful",
            "url": cls._get_url_of_object(location, cls._AWS_BUCKET_NAME, saved_file),
        }

    @classmethod
    def dump_objects(cls) -> Dict[str, Any]:
        s3 = cls._s3_resource
        client = cls._s3_client
        bucket = s3.Bucket(cls._AWS_BUCKET_NAME)
        location = client.get_bucket_location(Bucket=cls._AWS_BUCKET_NAME)[
            'LocationConstraint'
        ]

        objects = []

        for obj in bucket.objects.all():
            objects.append(
                cls._get_url_of_object(
                    location, cls._AWS_BUCKET_NAME, obj.key,
                ),
            )

        return {'objects': objects}

    @classmethod
    def delete_object_by_filename(cls, filename: str) -> Dict[str, Any]:
        try:
            object_key = filename

            s3 = cls._s3_client

            s3.delete_object(Bucket=cls._AWS_BUCKET_NAME, Key=object_key)

            return {"message": f"Object '{object_key}' deleted successfully."}

        except Exception as e:
            return {"error": f"Failed to delete object: {str(e)}"}
