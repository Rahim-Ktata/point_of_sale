from fastapi import APIRouter, Depends
from app.dependencies import DbDep
from app import crud, schemas, utils

router = APIRouter(
    prefix='/employee',
    tags=["Employee"]
)

@router.post("/add_employee", response_model=schemas.EmployeePublic)
async def add_employee(employee: schemas.EmployeeCreate, db: DbDep):
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
