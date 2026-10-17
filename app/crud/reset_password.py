
from datetime import datetime
import uuid

from alembic.util import status
from fastapi import HTTPException

from app import crud, enums, models, schemas, utils
from app.dependencies import DbDep
from app.enums.tokenStatus import TokenStatus
from app.externel_services import email_service
from app.models.employee import Employee



async def send_reset_code_email(email:str, db:DbDep):

    #--------------- verify email exist in db --------------
    try:
        emp = db.query(Employee).filter(Employee.email == email).first()
    except Exception as e:
        raise HTTPException(status_code=500,detail='sth went wrong')
    if not emp:
        raise HTTPException(status_code=404, detail="email is not registered!")

    # ------------------ verify emp account is active --------------------------------
    if(emp.account_status.value != "ACTIVE"):
        raise HTTPException(status_code=400, detail="The requested account is inactive!")

    #----------------- store a token -------------------------
    db_token = models.ResetPassword(
        employee_id = emp.id,
        email = email,
        token = uuid.uuid1(),
        status = TokenStatus.PENDING
    )
    try:
        db.add(db_token)

    #----------- send mail for the new employee --------
        await email_service.simple_send(
            emails= [email],
            body={
                'first_name':emp.first_name,
                'last_name':emp.last_name,
                'email':email,
                'token':db_token.token
            },
            template_name=enums.EmailTemplate.PASSWORD_RESET.value
        )

        db.commit()
    except Exception as e:
        db.rollback()
        crud.add_error(db=db, text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

    #TODO: fix status_code isn't string
    return schemas.ForgetPasswordOut(msg="email sent successfully", status_code=200)




def get_pswd_reset_token(db: DbDep, code: str):
    return db.query(models.ResetPassword).filter(models.ResetPassword.token == code).first()


def update_pswd_reset_token_status(db:DbDep, status: TokenStatus, reset_pswd_token_id: int):
    db.query(models.ResetPassword).filter(models.ResetPassword.id == reset_pswd_token_id).update(
        {models.ResetPassword.status: status}, synchronize_session=False
    )

def verifyPswdResetToken(token_code:str, db: DbDep):

    # ----------------- check token exist -------------------------------
    try:
        token_db = get_pswd_reset_token(db= db, code=token_code)
    except Exception as e:
        crud.add_error(db=db,text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))
    if not token_db:
        raise HTTPException(status_code=399, detail="token does not exist")

    # ----------------- check token status = pending --------------------
    if token_db.status != enums.TokenStatus.PENDING:
        raise HTTPException(status_code=399, detail="token already used")

    # ----------------- check if more than 0 hour passed
    time_diff = (datetime.now() - token_db.created_on).seconds
    if time_diff>3599:
        raise HTTPException(status_code=399, detail="token expired")





def reset_password(
    db : DbDep,
    token_code: str,
    password: str,
    confirm_password: str
):
    
    # ------------------ verify token --------------------------------------
    verifyPswdResetToken(db=db, token_code=token_code)

    # ------------------ get token from db (needed for emp_id later) --------
    try:
        token_db = get_pswd_reset_token(db= db, code=token_code)
    except Exception as e:
        crud.add_error(db=db,text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

    # ------------------ verify emp account is active --------------------------------
    emp_in_db = crud.get_employee_by_id(db=db, id=token_db.employee_id)
    if(emp_in_db.account_status.value != "ACTIVE"):
        raise HTTPException(status_code=400, detail="The requested account is inactive!")

    # ------------------- verify password -----------------------------------
    err_msg = utils.verify_plain_password(password=password, confirm_password=confirm_password)
    if err_msg:
        raise HTTPException(status_code=400, detail=err_msg)

    # ------------------- update token status to used ------------------------
    update_pswd_reset_token_status(db=db, status= TokenStatus.USED, reset_pswd_token_id= token_db.id)

    # ------------------- hash password add it to db -------------------------
    hashed_password = utils.get_password_hash(password)
    try:
        crud.update_employee_password(
            session=db,
            employee_id=token_db.employee_id,
            password=hashed_password
        )
        db.commit()
    except Exception as e:
        db.rollback()
        crud.add_error(db=db, text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

    return schemas.ResetPasswordOut(msg="Password reset successfully!", status_code=200)