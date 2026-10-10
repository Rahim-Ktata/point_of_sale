
# from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlmodel import Field, Session, SQLModel, create_engine, select
#
# from app import schemas, crud
#
# def get_session():
#     with Session(engine) as session:
#         yield session
#
# # @app.post("/add_employee/", response_model=schemas.EmployeePublic)
# @app.post("/add_employee/")
# def add_employee(employee: schemas.EmployeeCreate, session: Session = Depends(get_session)):
#     # skipped verification
#     #db_employee = Employee.model_validate(hero)
#     # in tuto we verify if user exists(with mail)
#
#     return crud.employee.create_employee(db= session, employee= employee)

