import json
import functions_framework
from dotenv import load_dotenv
from os import environ, path, getcwd, makedirs, listdir
import boto3
from botocore.exceptions import NoCredentialsError
from werkzeug.utils import secure_filename
import tempfile


load_dotenv()

AWS_PUB_KEY = environ.get("AWS_PUB_KEY")
AWS_PRIV_KEY = environ.get("AWS_PRIV_KEY")
AWS_BUCKET_NAME = environ.get("AWS_BUCKET_NAME")

def upload_to_s3(file, file_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_PUB_KEY,
                      aws_secret_access_key=AWS_PRIV_KEY)   
    
    try:
        tmpdir = tempfile.gettempdir()
        file.save(path.join(tmpdir, secure_filename(file.filename)))

        saved_file = file_name + "." + file.filename.rsplit('.')[1]
        s3.upload_file(f'{tmpdir}/{file.filename}', AWS_BUCKET_NAME, saved_file)

        location = s3.get_bucket_location(Bucket=AWS_BUCKET_NAME)['LocationConstraint']

        return json.dumps({"message":"Upload Successful", "url": get_url_of_obj(location, AWS_BUCKET_NAME, saved_file)}), 200

    except NoCredentialsError:
        return json.dumps({"message": "Process authentication failed"}), 500
    
    except FileNotFoundError:
        return json.dumps({"message": "File upload failed"}), 500
    
    except Exception as e:
        return json.dumps({"message": "Unexpected error", "exception": str(e)}), 500
    

def get_url_of_obj(loc, bucket_name, url_name):
    return "https://s3-%s.amazonaws.com/%s/%s" % (loc, bucket_name, url_name)


def dump_objects():
    session = boto3.Session(aws_access_key_id=AWS_PUB_KEY, aws_secret_access_key=AWS_PRIV_KEY)
    s3 = session.resource('s3')
    client = session.client('s3')
    bucket = s3.Bucket(AWS_BUCKET_NAME)
    location = client.get_bucket_location(Bucket=AWS_BUCKET_NAME)['LocationConstraint']

    objects = []

    for object in bucket.objects.all():
        objects.append(get_url_of_obj(location, AWS_BUCKET_NAME, object.key))

    return json.dumps({'message':objects})

@functions_framework.http
def object_uploader(request):

    if request.headers.get("Authorization") != environ.get("BEARER"):
        return json.dumps({"message": "Wrong or missing Bearer token"}), 401
    
    if (show := request.args.get('show')):
        return dump_objects() if show == "true" else json.dumps({"message": "show argument was not correctly set"})

    if not request.files:
        return json.dumps({"message": "No file has been transmitted"}), 400
    
    try:
        if request.form:
            data = request.form
        else:
            data = json.loads(request.data)

        filename=data["filename"]
    except:
        return json.dumps({"message": "filename not passed"}), 400

    return upload_to_s3(request.files["file"], filename)


