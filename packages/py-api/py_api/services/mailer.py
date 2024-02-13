from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from py_api.environment import HUB_MAIL, HUB_PSW


async def send_mail(receiver: str, subject: str, html: str) -> None:
    port = 465  # SSL
    email = HUB_MAIL
    password = HUB_PSW

    mime_msg = MIMEMultipart('alternative')

    mime_msg['From'] = email
    mime_msg['Subject'] = subject
    mime_msg.attach(MIMEText(html, "html"))

    async with SMTP(hostname='smtp.gmail.com', port=port, use_tls=True) as server:
        await server.login(email, password)
        await server.sendmail(email, receiver, mime_msg.as_string())


async def send_email_background_task(receiver: str, subject: str, html: str) -> None:
    await send_mail(receiver, subject, html)
