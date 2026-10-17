from sqlmodel import  Session
from app import enums
from fastapi import HTTPException
from datetime import datetime


def verifyToken(token_code:str, db: Session):
    from app.utils.errors import get_err_msg

    # ----------------- check token exist -------------------------------
    try:
        from app import crud
        token_db = crud.get_confirmation_token(db= db, code=token_code)
    except Exception as e:
        crud.add_error(db=db,text=str(e))
        raise HTTPException(status_code=500, detail=get_err_msg(str(e)))
    if not token_db:
        raise HTTPException(status_code=399, detail="token does not exist")

    # ----------------- check token status = pending --------------------
    if token_db.status != enums.TokenStatus.PENDING:
        raise HTTPException(status_code=399, detail="token already used")

    # ----------------- check if more than 0 hour passed
    time_diff = (datetime.now() - token_db.created_on).seconds
    if time_diff>3599:
        raise HTTPException(status_code=399, detail="token expired")
