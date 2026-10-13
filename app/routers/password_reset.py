
from fastapi import APIRouter, Depends
from app.dependencies import DbDep
from app import crud, schemas, utils

router = APIRouter(
    # prefix='/employee',
    tags=["Password Reset"]
)

@router.post("/forget_password", response_model=schemas.ForgetPasswordOut)
async def send_reset_pswd_email(email: str, db: DbDep):
    # return schemas.ForgetPasswordOut(msg='hi', status_code=1)
    return await crud.send_reset_code_email(email=email, db=db)


@router.post("/reset_password", response_model=schemas.ResetPasswordOut)
def reset_password(entry: schemas.ResetPasswordEntry, db: DbDep):

    return crud.reset_password(
        db = db,
        token_code=entry.token,
        password=entry.password,
        confirm_password=entry.confirm_password
    )
