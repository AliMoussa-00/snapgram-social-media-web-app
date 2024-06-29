#!/usr/bin/env python3
"""Mail server config."""

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.core.config import CONFIG


mail_conf = ConnectionConfig(
    MAIL_USERNAME=CONFIG.mail_username,
    MAIL_PASSWORD=CONFIG.mail_app_password,
    MAIL_FROM=CONFIG.mail_from,
    MAIL_PORT=CONFIG.mail_port,
    MAIL_SERVER=CONFIG.mail_server,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

mail = FastMail(mail_conf)


async def send_password_reset_email(email: str, token: str) -> None:
    """Send password reset email."""
    url: str = CONFIG.root_url + "/register/reset-password/" + token

    message = MessageSchema(
        recipients=[email],
        subject="SnapGram Password Reset",
        body=f"Click the link to reset your SnapGram account password: {url}\nIf you did not request this, please ignore this email",
        subtype=MessageType.plain,
    )

    await mail.send_message(message)
