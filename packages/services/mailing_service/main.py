import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import functions_framework
from dotenv import dotenv_values
import smtplib as smtp

config = dotenv_values('.env')


def send_mail(receiver, subject, html):
    port = 465  # SSL
    email = config['HUB_MAIL']
    password = config['HUB_PSW']

    mime_msg = MIMEMultipart('alternative')

    mime_msg['Subject'] = subject
    mime_msg.attach(MIMEText(html, "html"))

    server = smtp.SMTP_SSL('smtp.gmail.com', port)
    try:
        server.login(email, password)
        server.sendmail(email, receiver, mime_msg.as_string())

        server.close()

        return json.dumps({"message": "Email sent!"}), 200
    except Exception as e:
        return json.dumps({"message": e}), 500


@functions_framework.http
def handler(request):
    if request.form:
        data = request.form
    else:
        data = json.loads(request.data)

    html = data["html"]
    subject = data["subject"]
    receiver = data["receiver"]

    return send_mail(receiver, subject, html)
