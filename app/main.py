from fastapi import BackgroundTasks, FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import crud, schemas, database, utils
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import  Session
from app import models


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

def fake_hash_password(password: str):
    return "fakehashed" + password

# class User()
# class UserInDB()

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/hi")
def hi(token: str = Depends(oauth2_scheme)):
    return {token:token}


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