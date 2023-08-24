from os import getenv, path
from tempfile import gettempdir
from typing import Any, Dict

import boto3
from dotenv import load_dotenv
from fastapi import Request, UploadFile

load_dotenv()

AWS_PUB_KEY = getenv("AWS_PUB_KEY", "")
AWS_PRIV_KEY = getenv("AWS_PRIV_KEY", "")
AWS_BUCKET_NAME = getenv("AWS_BUCKET_NAME", "")


class UploaderControllers:
    @classmethod
    def get_url_of_object(cls, location: str, bucket_name: str, url_name: str) -> str:
        return "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, url_name)

    @classmethod
    def upload_object(cls, request: Request, file: UploadFile) -> Dict[str, Any]:
        s3 = boto3.client(
            's3', aws_access_key_id=AWS_PUB_KEY,
            aws_secret_access_key=AWS_PRIV_KEY,
        )

        file_name = request.body["filename"]

        try:
            tmpdir = gettempdir()
            file.save(path.join(tmpdir, file.filename))

            saved_file = file_name + "." + file.filename.rsplit('.')[1]
            s3.upload_file(
                f'{tmpdir}/{file.filename}',
                AWS_BUCKET_NAME, saved_file, ExtraArgs={'ContentType': 'image/jpeg'},
            )

            location = s3.get_bucket_location(Bucket=AWS_BUCKET_NAME)[
                'LocationConstraint'
            ]

            return {"message": "Upload Successful", "url": cls.get_url_of_obj(location, AWS_BUCKET_NAME, saved_file)}

        # except NoCredentialsError:
        #     return json.dumps({"message": "Process authentication failed"}), 500

        # except FileNotFoundError:
        #     return json.dumps({"message": "File upload failed"}), 500

        except:
            pass

    @classmethod
    def dump_objects(cls) -> Dict[str, Any]:
        session = boto3.Session(
            aws_access_key_id=AWS_PUB_KEY,
            aws_secret_access_key=AWS_PRIV_KEY,
        )
        s3 = session.resource('s3')
        client = session.client('s3')
        bucket = s3.Bucket(AWS_BUCKET_NAME)
        location = client.get_bucket_location(Bucket=AWS_BUCKET_NAME)[
            'LocationConstraint'
        ]

        objects = []

        for obj in bucket.objects.all():
            objects.append(
                cls.get_url_of_object(
                    location, AWS_BUCKET_NAME, obj.key,
                ),
            )

        return {'objects': objects}
