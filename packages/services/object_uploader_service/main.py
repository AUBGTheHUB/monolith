import json
import functions_framework
from dotenv import load_dotenv
from os import environ, path, getcwd, makedirs, listdir
import boto3
from botocore.exceptions import NoCredentialsError
from werkzeug.utils import secure_filename


load_dotenv()

AWS_PUB_KEY = environ.get("AWS_PUB_KEY")
AWS_PRIV_KEY = environ.get("AWS_PRIV_KEY")
AWS_BUCKET_NAME = environ.get("AWS_BUCKET_NAME")

def upload_to_s3(file, file_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_PUB_KEY,
                      aws_secret_access_key=AWS_PRIV_KEY)   
    
    try:
        file.save(path.join(getcwd(), secure_filename(file.filename)))
        s3.upload_file(f'{getcwd()}/{file.filename}', AWS_BUCKET_NAME, file_name)

        return json.dumps({"message":"Upload Successful"}), 200

    except FileNotFoundError:
        return json.dumps({"message": "File upload failed"}), 500

    except NoCredentialsError:
        return json.dumps({"message": "Process authentication failed"}), 500


@functions_framework.http
def object_uploader(request):
    if request.headers.get("Authorization") != environ.get("BEARER"):
        return json.dumps({"message": "Wrong or missing Bearer token"}), 401

    if not request.files:
        return json.dumps({"message": "No file has been transmitted"}), 400
    
    if request.form:
        data = request.form
    else:
        data = json.loads(request.data)

    if not data and data["filename"]:
        return json.dumps({"message": "filename was not passed"}), 400

    return upload_to_s3(request.files["file"], data["filename"])

