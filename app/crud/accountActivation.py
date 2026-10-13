
from app import models, schemas, crud, enums, utils
from fastapi import FastAPI, Depends, status, HTTPException
from app.models import Employee, AccountActivation
from sqlalchemy.orm import Session
from app.externel_services import email_service
from app.enums import AccountStatus, TokenStatus

# try catch whenever u call one of those crud``
def get_confirmation_token(db: Session, code: str):
    return db.query(models.AccountActivation).filter(models.AccountActivation.token == code).first()

def update_employee_account_status(db:Session, status: AccountStatus, employee_id: int):
    db.query(Employee).filter(Employee.id == employee_id).update(
        {Employee.account_status: status}, synchronize_session=False
    )

def update_token_status(db:Session, status: TokenStatus, account_activation_id: int):
    db.query(AccountActivation).filter(AccountActivation.id == account_activation_id).update(
        {AccountActivation.status: status}, synchronize_session=False
    )

def update_employee_password(session:Session, employee_id:int, password:str):
    session.query(Employee).filter(Employee.id == employee_id).update(
        {Employee.password: password}, synchronize_session=False
    )

def update_account_status_and_pswd(session : Session, token_code:str, password:AccountActivation.password, confirm_password:AccountActivation.confirm_password):

    try:
        token_db = crud.get_confirmation_token(db= session, code=token_code)
        # ----------------- update the account status to active -------------
        crud.update_employee_account_status(db=session, status= enums.AccountStatus.ACTIVE, employee_id= token_db.employee_id)
        # ----------------- update the token status to used -------------
        crud.update_token_status(db=session, status=enums.TokenStatus.USED, account_activation_id=token_db.id)
    except Exception as e:
        session.rollback()
        crud.add_error(db=session, text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

    # ---------------- PSWD ------------------------------------------------
    # ----------------------------------------------------------------------
    # ------------------ verify password ------------------------------------
    err_msg = utils.verify_plain_password(password=password, confirm_password=confirm_password)
    if err_msg:
        raise HTTPException(status_code=400, detail=err_msg)
    # ------------------- hash password add it to db -------------------------
    hashed_password = utils.get_password_hash(password)
    try:
        crud.update_employee_password(session=session, employee_id=token_db.employee_id,password=hashed_password)
    except Exception as e:
        session.rollback()
        crud.add_error(db=session, text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

    session.commit()

    return schemas.AccountActivationOut(msg="account confirmed", status_code=status.HTTP_200_OK)
