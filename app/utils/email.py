from email.message import EmailMessage

import aiosmtplib

from app.config import (
    GMAIL_APP_PASSWORD,
    GMAIL_SMTP_HOST,
    GMAIL_SMTP_PORT,
    GMAIL_USER,
)


async def send_activation_email(to_email: str, activation_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Activate your account"
    msg["From"] = GMAIL_USER
    msg["To"] = to_email
    msg.set_content(f"Click the link to activate your account: {activation_link}")

    await aiosmtplib.send(
        msg,
        hostname=GMAIL_SMTP_HOST,
        port=GMAIL_SMTP_PORT,
        username=GMAIL_USER,
        password=GMAIL_APP_PASSWORD,
        start_tls=True,
    )
