
from app.schemas.accountActivation import MyBaseModel

class ForgetPasswordOut(MyBaseModel):
    msg: str
    status_code: str

class ResetPasswordEntry(MyBaseModel):
    token : str
    password : str
    confirm_password : str

class ResetPasswordOut(MyBaseModel):
    msg: str
    status_code: str