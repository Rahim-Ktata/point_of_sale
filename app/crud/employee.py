
import uuid
from typing import List
from app import models, schemas, utils, crud
from app import enums
from app.enums import TokenStatus
from fastapi import FastAPI, Depends, status, HTTPException
from app.models import Employee, EmployeeRole

from sqlalchemy.orm import Session
from app.externel_services import email_service


def get_employee_by_id(db: Session, id: int):
    return db.query(models.Employee).filter(models.Employee.id == id).first()

def get_employee_by_email(db: Session, email: str):
    # select * from employee where id = id limit 1
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def get_employee_roles(db: Session, employee_id: str):
    return db.query(models.EmployeeRole).filter(models.EmployeeRole.employee_id == employee_id).all()

# skip & limit : used for pagination
def get_all_employees(db: Session, skip: int = 0, limit: int = 100):
    try:
        employees_db =  db.query(models.Employee).offset(skip).limit(limit).all()
        employees_out = []
        for emp in employees_db:
            emp_data = emp.__dict__
            emp_data.pop('password')
            emp_roles_db = emp.roles
            emp_data.pop('roles')
            # emp_roles_db = get_employee_roles(db=db, employee_id=emp.id)
            emp_roles = []
            for role in emp_roles_db:
                emp_roles.append(role.role)
            employees_out.append(schemas.EmployeePublic(**emp_data, roles=emp_roles))

        total_records = db.query(models.Employee).count()

        number_of_pages = total_records // limit
        if(total_records % limit):number_of_pages+=1
    except Exception as e:
        crud.add_error(db=db,text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))
    return schemas.GetAllEmployees(
        page_number=(skip//limit)+1,
        page_size=limit,
        employees=employees_out,
        total_records=total_records,
        number_of_pages=number_of_pages
    )



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
        await email_service.simple_send(
            emails= [employee.email],
            body={**employee_data,'token':db_token.token},
            template_name=enums.emailTemplates.EmailTemplate.ACCOUNT_ACTIVATION.value
        )

        db.commit()


    except Exception as e:
        db.rollback()
        crud.add_error(db=db,text=str(e))
        raise HTTPException(status_code=400, detail=utils.get_err_msg(str(e)))

    return schemas.EmployeePublic(
        **employee_data,
        id=db_employee.id,
        roles=employee_roles,
        created_on=db_employee.created_on
    )


def edit_employee(employee_id:int, entry:schemas.EditEmployeeEntry, db:Session):

    # -------------- check employee exist in db --------------------------------
    try:
        emp_in_db= get_employee_by_id(db=db,id=employee_id)
    except Exception as e:
        crud.add_error(db=db, text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))
    if not emp_in_db:
        raise HTTPException(status_code=400, detail="employee doesn't exist")

    # --------------- update the emp data -------------------------------------
    emp_new_data = entry.model_dump()
    emp_new_roles = emp_new_data.pop('roles')

    try:
        db.query(Employee).filter(Employee.id == employee_id).update(
            emp_new_data, synchronize_session=False
        )
    except Exception as e:
        crud.add_error(db=db, text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

    # --------------- update roles -------------------------------------
        # ------------ delete old ones ---------------------------------
    try:
        old_role = 1
        while(old_role):
            old_role = db.query(EmployeeRole).filter(EmployeeRole.employee_id == employee_id).first()
            if(old_role):
                db.delete(old_role)
            # ------------ add new ones ---------------------------------
        
        for role in emp_new_roles:
            db.add(EmployeeRole(employee_id=employee_id, role=role))
        
        db.commit()
    except Exception as e:
        db.rollback()
        crud.add_error(db=db, text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

    return schemas.EditEmployeeOut(msg="employee data updated", status_code='200')
