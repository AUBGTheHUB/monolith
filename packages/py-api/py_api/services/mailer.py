from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ

from aiosmtplib import SMTP


async def send_mail(receiver: str, subject: str, html: str) -> None:
    port = 465  # SSL
    email = environ["HUB_MAIL"]
    password = environ["HUB_PSW"]

    mime_msg = MIMEMultipart('alternative')

    mime_msg['From'] = email
    mime_msg['Subject'] = subject
    mime_msg.attach(MIMEText(html, "html"))

    async with SMTP(hostname='smtp.gmail.com', port=port, use_tls=True) as server:
        await server.login(email, password)
        await server.sendmail(email, receiver, mime_msg.as_string())
