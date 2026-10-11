from typing import List

from fastapi import FastAPI
from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.config import settings


# class EmailSchema(BaseModel):
#     email: List[NameEmail]


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER = Path(__file__).parent.parent / 'templates',
)

app = FastAPI()


# @app.post("/email")
async def simple_send(emails: list[NameEmail], body:dict) -> JSONResponse:
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=emails,
        template_body=body,
        subtype=MessageType.html,
    )
    await FastMail(conf).send_message(message,template_name="email_template.html")
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
