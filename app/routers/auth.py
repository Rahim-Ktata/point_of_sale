from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import DbDep
from app import schemas
from app.utils.Oauth2 import authenticate_emp, create_access_token
from app.config import settings

router = APIRouter(
    # prefix='/auth',
    tags=["Auth"]
)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    db:DbDep,
    form_data: OAuth2PasswordRequestForm=Depends()
) -> schemas.Token:
    emp = authenticate_emp(db=db, email=form_data.username, password=form_data.password)
    if not emp:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
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