from __future__ import annotations
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from core.config import settings

class MailService:
    _config = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=True,
    )

    @classmethod
    async def send(cls, *, recipient: str, subject: str, body: str) -> None:
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype="html",
        )

        mailer = FastMail(cls._config)
        await mailer.send_message(message)

    @classmethod
    async def send_verification_email(cls, *, recipient: str, username: str, verification_url: str) -> None:
        body = f"""
        <h2>Hello {username}</h2>

        <p>Welcome to DataSage.</p>

        <p>Please verify your email address by clicking below.</p>

        <p>
            <a href="{verification_url}">Verify Email</a>
        </p>
        """

        await cls.send(recipient=recipient, subject="Verify your email", body=body)

    @classmethod
    async def send_password_reset_email(cls, *, recipient: str, username: str, reset_url: str) -> None:
        body = f"""
        <h2>Hello {username}</h2>

        <p>Click below to reset your password.</p>

        <p>
            <a href="{reset_url}">Reset Password</a>
        </p>
        """

        await cls.send(recipient=recipient, subject="Password Reset", body=body)

    @classmethod
    async def send_payment_success_email(cls, *, recipient: str, username: str, plan_name: str) -> None:
        body = f"""
        <h2>Hello {username}</h2>

        <p>Your payment was successful.</p>

        <p>
            Your <strong>{plan_name}</strong> subscription
            has been activated.
        </p>

        <p>Thank you for your purchase.</p>
        """

        await cls.send(recipient=recipient, subject="Subscription Activated", body=body)