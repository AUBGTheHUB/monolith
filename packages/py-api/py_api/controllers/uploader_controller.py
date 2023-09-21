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

    @classmethod
    def _get_url_of_object(cls, location: str, bucket_name: str, url_name: str) -> str:
        return "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, url_name)

    @classmethod
    def upload_object(cls, file: UploadFile, file_name: str) -> Dict[str, Any]:
        s3 = boto3.client(
            's3', aws_access_key_id=cls._AWS_PUB_KEY,
            aws_secret_access_key=cls._AWS_PRIV_KEY,
        )

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
        session = boto3.Session(
            aws_access_key_id=cls._AWS_PUB_KEY,
            aws_secret_access_key=cls._AWS_PRIV_KEY,
        )
        s3 = session.resource('s3')
        client = session.client('s3')
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
    def delete_object(cls, image_url: str) -> Dict[str, Any]:
        try:
            parts = image_url.split('/')
            if len(parts) < 4:
                return {"error": "Invalid URL format"}

            object_key = '/'.join(parts[3:])

            s3 = boto3.client(
                's3', aws_access_key_id=cls._AWS_PUB_KEY,
                aws_secret_access_key=cls._AWS_PRIV_KEY,
            )

            s3.delete_object(Bucket=cls._AWS_BUCKET_NAME, Key=object_key)

            return {"message": f"Object '{object_key}' deleted successfully."}

        except Exception as e:
            return {"error": f"Failed to delete object: {str(e)}"}
