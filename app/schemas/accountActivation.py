
from pydantic import BaseModel

class MyBaseModel(BaseModel):
    class config:
        orm_mode = True

class AccountActivation(MyBaseModel):
    token : str
    password : str
    confirm_password : str

class AccountActivationOut(MyBaseModel):
    msg : str
    status_code: int

