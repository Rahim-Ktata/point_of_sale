
from app.schemas.common import MyBaseModel, Response


class Token(Response):
    access_token: str
    token_type: str


class TokenData(MyBaseModel):
    email: str | None = None