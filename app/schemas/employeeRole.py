
from pydantic import BaseModel
from app.enums import ContractType, Gender, AccountStatus, Role
from datetime import date, datetime
from typing import List


class MyBaseModel(BaseModel):
    class config:
        orm_mode = True

class EmployeeRole(MyBaseModel):

    employee_id : int
    role : Role

