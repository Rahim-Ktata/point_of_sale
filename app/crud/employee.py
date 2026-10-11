
import uuid
from typing import List
from app import models, schemas, utils, crud
from app.enums import TokenStatus
from fastapi import FastAPI, Depends, status, HTTPException

from sqlalchemy.orm import Session
from app.utils import emailUtil


def get_employee_by_id(db: Session, id: int):
    # select * from employee where id = id limit 1
    return db.query(models.Employee).filter(models.Employee.id == id).first()

def get_employee_by_email(db: Session, email: str):
    # select * from employee where id = id limit 1
    return db.query(models.Employee).filter(models.Employee.email == email).first()

# skip & limit : used for pagination
def get_all_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()

def get_employee_roles(db: Session, employee_id: str):
    return db.query(models.EmployeeRole).filter(models.EmployeeRole.employee_id == employee_id).all()

async def create_employee(db: Session, employee: schemas.EmployeeCreate):

    # model_dump : convert to dict
    employee_data = employee.model_dump()
    employee_roles = employee_data.pop("roles")

    try:
        #---------------- add employee to db ---------------
        db_employee = models.Employee(**employee_data)
        db.add(db_employee)
        db.flush() # the employee id exists now

        #----------------- add roles to db -----------------
        for role in employee_roles:
            db_role = models.EmployeeRole(employee_id = db_employee.id, role=role)
            db.add(db_role)

        #----------- store a token -------------------------
        db_token = models.AccountActivation(
            employee_id = db_employee.id,
            email = db_employee.email,
            token = uuid.uuid1(),
            status = TokenStatus.PENDING
        )
        db.add(db_token)

        #----------- send mail for the new employee --------
        #TODO: make this done after the commit with possibility to resend
        await emailUtil.simple_send(emails= [employee.email], body={**employee_data,'token':db_token.token})

        #return schemas.EmployeePublic(**db_employee.__dict__, roles=employee_roles)
        db.commit()
        return db_employee

    except Exception as e:
        db.rollback()
        crud.add_error(db=db,text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))



