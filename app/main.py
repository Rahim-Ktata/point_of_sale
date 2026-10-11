from fastapi import FastAPI, Depends
from app.utils.Oauth2 import get_current_active_emp
from . import schemas
from fastapi.middleware.cors import CORSMiddleware
from .routers import employee,employee_bulk_upload


app = FastAPI()
app.include_router(employee.router)
app.include_router(employee_bulk_upload.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

#TODO: change the logic of active | inactive : if an emp is inactive , don't give him
# a jwt token that way u re not adding mutable data to the token?
#TODO: if an account deactivated by admin the jwt must be updated => it can't be stateless ??
#NOTE: the tuto flow visit db on each request, it doesnt go with server only flow
# and that fits the app better so i can check if the account is active on each request


@app.get("/")
def main():
    pass