import logging
import smtplib
from email.message import EmailMessage

from ..config import Settings

logger = logging.getLogger(__name__)


def send_notification(settings: Settings, subject: str, body: str) -> bool:
    if not all((settings.smtp_host, settings.smtp_username, settings.smtp_password, settings.notification_email)):
        logger.info("SMTP is not configured; notification skipped.")
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.smtp_username
    message["To"] = settings.notification_email
    message.set_content(body)
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.send_message(message)
        return True
    except (OSError, smtplib.SMTPException):
        logger.exception("SMTP notification failed.")
        return False
