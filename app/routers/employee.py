from fastapi import APIRouter, Depends
from app.dependencies import DbDep, OauthDep
from app import crud, schemas, utils

router = APIRouter(
    prefix='/employee',
    tags=["Employee"]
)

@router.post("/add_employee", response_model=schemas.EmployeePublic)
async def add_employee(employee: schemas.EmployeeCreate, db: DbDep, current_emp: OauthDep):
    return await crud.create_employee(db= db, employee= employee)


@router.patch("/confirm_account")
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
def get_employees(db:DbDep, current_emp: OauthDep, skip: int =0, limit: int =15):
    return crud.get_all_employees(db=db, skip=skip, limit=limit)