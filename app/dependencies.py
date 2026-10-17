
from fastapi.security import OAuth2PasswordBearer 
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app import database, schemas
from app.utils.Oauth2 import get_current_active_emp

def get_session():
    with Session(database.engine) as session:
        yield session

# DbDep : Session = Depends(get_session)
DbDep = Annotated[Session, Depends(get_session)]
OauthDep = Annotated[schemas.EmployeeInDB, Depends(get_current_active_emp)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")