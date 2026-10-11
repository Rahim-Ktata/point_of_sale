

from app.config import settings

from jwt.exceptions import InvalidTokenError
from alembic.util import status
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
import jwt

from app import crud, enums, schemas
from app.dependencies import DbDep, oauth2_scheme
from app.utils.password import verify_hashed_password


def get_emp(email:str, db: DbDep):
    try:
        emp = crud.get_employee_by_email(db=db,email=email)
    except Exception as e:
        raise HTTPException(status_code=404,detail="sth went wrong")
    if emp:
        try:
            roles = crud.get_employee_roles(db=db,employee_id=emp.id)
        except Exception as e:
            raise HTTPException(status_code=404,detail="sth went wrong")

        roles_list = []
        for role in roles:
            roles_list.append(role.role.value)
        keys = list(emp.__dict__.keys())
        needed_keys = []
        for key in keys:
            if(key[0]!='_' and key!='roles'):
                needed_keys.append(key)
        emp_data = {}
        emp_data['roles']= roles_list
        for key in needed_keys:
            emp_data[key]=getattr(emp,key)

        return schemas.EmployeeInDB(**emp_data)


def authenticate_emp(email: str, password: str, db: DbDep):
    emp = get_emp(db=db, email=email)
    if not emp:
        # verify_password(password, DUMMY_HASH)
        return False
    if not verify_hashed_password(plain_password=password, hashed_password=emp.password):
        return False
    return emp

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

async def get_current_emp(db:DbDep, token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
        # TODO: add the rest of info from payload to the TokenData
        token_data = schemas.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    emp = get_emp(db=db, email=token_data.email)
    if emp is None:
        raise credentials_exception
    return emp

async def get_current_active_emp(
    current_emp: schemas.EmployeeInDB = Depends(get_current_emp) ,
):
    if current_emp.account_status == enums.AccountStatus.INACTIVE:
        raise HTTPException(status_code=400, detail="Inactive account")
    return current_emp


