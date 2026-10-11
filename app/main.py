from datetime import datetime, timedelta, timezone
from alembic.util import status
from fastapi import BackgroundTasks, FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import crud, schemas, database, utils
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import  Session
from app import enums, models
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError



def get_session():
    with Session(database.engine) as session:
        yield session
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#############################################################################################



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TODO: access from .env
SECRET_KEY = "3feca2ed9ab61a17df0c5a89056bb6fa1ee3e1839c34658b0c1b60a52bf81db8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))


def get_password_hash(password):
    return password_hash.hash(password)


def get_emp(email:str, db: Session = Depends(get_session)):
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


def authenticate_emp(email: str, password: str, db: Session = Depends(get_session)):
    emp = get_emp(db=db, email=email)
    if not emp:
        # verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(plain_password=password, hashed_password=emp.password):
        return False
    return emp


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_emp(token:str = Depends(oauth2_scheme), db:Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm=Depends(),
    db:Session = Depends(get_session)
) -> schemas.Token:
    emp = authenticate_emp(db=db, email=form_data.username, password=form_data.password)
    if not emp:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_keys = [
            "first_name",
            "last_name",
            "email",
            "number",
            "birth_date",
            "address",
            "cnss_number",
            "contract_type",
            "gender",
            "account_status",
            "phone_number",
            "created_on",
            "roles",
            "id",
        ]
    payload_data = {}
    for key in payload_keys:
        payload_data[key]= getattr(emp, key)
    payload_data['birth_date'] = payload_data["birth_date"].isoformat()
    payload_data['created_on'] = payload_data['created_on'].isoformat()
    payload_data['contract_type']= payload_data['contract_type'].value
    payload_data['account_status']= payload_data['account_status'].value
    payload_data['gender']= payload_data['gender'].value
    for role in payload_data['roles']:
        role = role.value
    payload_data['roles'] = ' '.join(payload_data['roles'])
    access_token = create_access_token(
        data=payload_data, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/")
async def read_users_me(
    current_emp: schemas.EmployeeInDB = Depends(get_current_active_emp),
) -> schemas.EmployeeInDB:
    return current_emp


@app.get("/users/me/items/")
async def read_own_items(
    current_user: schemas.EmployeeInDB= Depends(get_current_active_emp),
):
    return [{"item_id": "Foo", "owner": current_user.first_name}]


#############################################################################################



@app.post("/add_employee", response_model=schemas.EmployeePublic)
async def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_session)):

    return await crud.create_employee(db= db, employee= employee)


@app.patch("/confirm_account")
def account_confirmation(accountActivation: schemas.AccountActivation, session: Session = Depends(get_session)):

    #TODO: fix this chaos, the goal is to rollback on partial success
    utils.verifyToken(session=session, token_code=accountActivation.token)
    return crud.update_account_status_and_pswd(session = session, token_code=accountActivation.token, password=accountActivation.password, confirm_password=accountActivation.confirm_password)


@app.get("/employees/possibleFields")
def get_possible_import_fields(session: Session = Depends(get_session)):
    return schemas.ImportPossibleFields(possible_fields=utils.options)


@app.post("/employees/bulkUpload")
async def employees_validation_and_bulk_upload(entry: schemas.MatchyUploadEntry, background_tasks:BackgroundTasks ,session: Session = Depends(get_session)):
    employees = entry.lines
    force_upload = entry.force_upload
    # a whole column is missing (so we can verify employees[0] only)
    missing_mandatory_fields = list(set(utils.mandatory_fields.keys()) - set(employees[0].keys()))

    if missing_mandatory_fields:
        missing_fields_names = [utils.mandatory_fields[val] for val in missing_mandatory_fields]
        raise HTTPException(status_code=400, detail=f"missing mandatory fields: { ', '.join(missing_fields_names) }")

    return utils.validate_employees_data_and_upload(employees=employees, background_tasks= background_tasks,force_upload=entry.force_upload, db=session)


@app.get("/")
def main():
    pass