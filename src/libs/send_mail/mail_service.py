from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.commons.configs.config import get_app_settings
from src.commons.constants.message import ERROR_MESSAGE
from src.commons.middlewares.exception import AppExceptionCase
from src.commons.utils.template import render_template

settings = get_app_settings()


class SendMailService:

    conf = ConnectionConfig(
        MAIL_USERNAME=settings.email_user,
        MAIL_PASSWORD=settings.email_password,
        MAIL_PORT=settings.email_port,
        MAIL_SERVER=settings.email_host,
        MAIL_TLS=True,
        MAIL_SSL=False,
    )

    @staticmethod
    async def send_email_forgot_password(**kwargs):
        try:
            message = MessageSchema(
                subject="Reset Password", recipients=[kwargs["email"]], subtype="html"
            )

            message.body = render_template(
                template_name_or_list="forgot-password.html",
                context={"new_password": kwargs["new_password"]},
            )

            fm = FastMail(SendMailService.conf)
            await fm.send_message(message)
        except Exception as e:
            raise AppExceptionCase(
                context={"reason": ERROR_MESSAGE.SEND_MAIL_ERROR, "code": e.code},
                status_code=500,
            )
