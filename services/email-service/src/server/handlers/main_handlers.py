import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from result import Err
from structlog.stdlib import get_logger

LOG = get_logger()


class MainHandlers:

    @staticmethod
    async def send_mail(receiver: str, subject: str, text: str) -> Err[Exception]:
        port = 465  # SSL
        email = os.environ["HUB_MAIL"]
        password = os.environ["HUB_PSW"]

        mime_msg = MIMEMultipart("alternative")

        mime_msg["From"] = email
        mime_msg["Subject"] = subject
        # TODO make this html potentially
        mime_msg.attach(MIMEText(text, "text"))
        try:
            async with SMTP(hostname="smtp.gmail.com", port=port, use_tls=True) as server:
                LOG.debug("Logging into Gmail")
                await server.login(email, password)
                LOG.info("Sending email to {}".format(receiver))
                await server.sendmail(email, receiver, mime_msg.as_string())
        except Exception as e:
            LOG.exception("Sending of email failed due to err {}".format(e))
            return Err(e)
