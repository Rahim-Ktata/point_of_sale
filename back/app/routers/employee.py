from fastapi import APIRouter, Depends
from app.dependencies import DbDep, OauthDep
from app import crud, schemas, utils

router = APIRouter(
    prefix='/employee',
    tags=["Employee"]
)

@router.post("/add_employee", response_model=schemas.EmployeePublic)
async def add_employee(employee: schemas.EmployeeCreate, db: DbDep, current_emp: OauthDep):
# async def add_employee(employee: schemas.EmployeeCreate, db: DbDep):
    return await crud.create_employee(db= db, employee= employee)


@router.patch("/confirm_account", response_model=schemas.AccountActivationOut)
def account_confirmation(accountActivation: schemas.AccountActivation, db: DbDep):

    utils.verifyToken(db=db, token_code=accountActivation.token)
    #TODO: rename session to db
    return crud.update_account_status_and_pswd(
        session = db,
        token_code=accountActivation.token,
        password=accountActivation.password,
        confirm_password=accountActivation.confirm_password
    )

@router.patch("/edit_employee/{employee_id}", response_model=schemas.EditEmployeeOut)
def edit_employee(employee_id: int, entry:schemas.EditEmployeeEntry, db:DbDep, current_emp: OauthDep):
    return crud.edit_employee(
        employee_id=employee_id,
        entry= entry, 
        db= db    
    )

@router.get("/get_all_employees", response_model=schemas.GetAllEmployees)
def get_employees(db:DbDep, current_emp: OauthDep, skip: int =0, limit: int =15, filter: str=''):
    return crud.get_all_employees(db=db, skip=skip, limit=limit, filter=filter)
    # return {
    #     "page_number":1 ,
    #     "page_size":1 ,
    #     "number_of_pages": 1,
    #     "total_records": 1,
    #     "employees":[]
    # }


@router.delete("/delete_employee/{employee_id}", response_model=schemas.DeleteEmployeeResponse)
def delete_employee(db:DbDep, employee_id:int, x:OauthDep):
    return crud.delete_employee(db=db,employee_id=employee_id)