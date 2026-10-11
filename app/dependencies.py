
from fastapi.security import OAuth2PasswordBearer 
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app import database

def get_session():
    with Session(database.engine) as session:
        yield session

# DbDep : Session = Depends(get_session)
DbDep = Annotated[Session, Depends(get_session)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")