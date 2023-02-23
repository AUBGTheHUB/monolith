import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import functions_framework
from dotenv import load_dotenv
import smtplib as smtp
from os import environ

load_dotenv()


@functions_framework.http
def object_uploader(request):

    if request.headers.get("Authorization") != environ.get("BEARER"):
        return json.dumps({"message": "Wrong or missing Bearer token"}), 401

    if not request.files:
        return json.dumps({"message": "No file has been transmitted"}, 400)

