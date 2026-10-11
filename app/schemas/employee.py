
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

class EmployeeInDB(EmployeeBase):
    id: int  
    password: str | None
    created_on: datetime
    roles: List[Role]


class EmployeePublic(EmployeeBase):
    id: int


class EmployeeCreate(EmployeeBase):
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
