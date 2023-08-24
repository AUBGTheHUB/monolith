from os import getenv
from typing import Any, Dict

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_PUB_KEY = getenv("AWS_PUB_KEY", "")
AWS_PRIV_KEY = getenv("AWS_PRIV_KEY", "")
AWS_BUCKET_NAME = getenv("AWS_BUCKET_NAME", "")


class UploaderControllers:
    @classmethod
    def get_url_of_object(cls, location: str, bucket_name: str, url_name: str) -> str:
        return "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, url_name)

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
