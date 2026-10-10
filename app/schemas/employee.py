
from pydantic import BaseModel
from app.enums import ContractType, Gender, AccountStatus, Role
from datetime import date, datetime
from typing import List


class MyBaseModel(BaseModel):
    class config:
        orm_mode = True


class EmployeeBase(MyBaseModel):

    first_name : str
    last_name : str
    email : str
    number : int
    birth_date : date
    address : str | None = None
    cnss_number : str | None = None
    contract_type : ContractType
    gender : Gender
    account_status : AccountStatus = AccountStatus.INACTIVE
    phone_number : str | None = None


class Employee(EmployeeBase):
    # id: int | None = Field(default=None, primary_key=True)
    # secret_name: str
    pass

class EmployeePublic(EmployeeBase):
    id: int


class EmployeeCreate(EmployeeBase):
    # the password can be null cuz admin create employee account,
    # the employee gets mail and sets his password
    # password : str | None = None
    # confirm_password : str | None = None
    created_on : datetime
    roles: List[Role]


class EmployeeUpdate(EmployeeBase):
    # name: str | None = None
    # age: int | None = None
    # secret_name: str | None = None
    pass


class EmployeeUploadResponse(MyBaseModel):
    errs : List[str] = []
    warnings : List[str] = []
    detail: str = ""
    stautus_code: int | None = None
