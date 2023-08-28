from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv
from smtplib import SMTP_SSL


async def send_mail(receiver: str, subject: str, html: str) -> None:
    port = 465  # SSL
    email = getenv('HUB_MAIL', '')
    password = getenv('HUB_PSW', '')

    mime_msg = MIMEMultipart('alternative')

    # TODO: Add sender
    mime_msg['Subject'] = subject
    mime_msg.attach(MIMEText(html, "html"))

    server = SMTP_SSL('smtp.gmail.com', port)
    server.login(email, password)
    server.sendmail(email, receiver, mime_msg.as_string())

    server.close()
