import copy
from fastapi.testclient import TestClient
from app import models
from app.main import app
from app.tests.conftest import get_emp_account_activation_token

client = TestClient(app)

data= {
    "first_name": "Rahim",
    "last_name": "ktata",
    "email": "abdrrahimktata@gmail.com",
    "number": 0,
    "birth_date": "2026-10-15",
    "address": "address",
    "cnss_number": "12345678-12",
    "contract_type": "CDI",
    "gender": "MALE",
    "account_status": "INACTIVE",
    "phone_number": "12345678",
    "roles": [
        "ADMIN","VENDOR"
    ]
}



# -------------------- /employee/add_employee -------------------------

def test_add_employee(test_db):
    response = client.post(
        "/employee/add_employee",
        json= data
    )
    assert response.status_code == 200

    res = response.json()
    assert res["created_on"] is not None
    assert res["id"] == 1
    assert len(res["roles"]) == 2


def test_add_employee_wrong_email(test_db):
    wrong_data= copy.deepcopy(data)
    wrong_data["email"] = "a"

    response = client.post(
        "/employee/add_employee",
        json= wrong_data
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid email address'}


def test_add_employee_wrong_phone_number(test_db):
    wrong_data= copy.deepcopy(data)
    wrong_data["phone_number"] = "a"

    response = client.post(
        "/employee/add_employee",
        json= wrong_data
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Phone number should be 8 digits"}


def test_add_employee_wrong_cnss_number(test_db):
    wrong_data= copy.deepcopy(data)
    wrong_data["cnss_number"] = "a"

    response = client.post(
        "/employee/add_employee",
        json= wrong_data
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Cnss number should be {8 digits}-{2 digits} and it's Mandatory for Cdi and Cdd"
    }


# -------------------- /employee/confirm_account -------------------------

def test_confirm_account(test_db):
    client.post(
        "/employee/add_employee",
        json = data
    )
    token = get_emp_account_activation_token(test_db)
    confirm_entry = {
        "token": token,
        "password": "rahim123",
        "confirm_password": "rahim123"
    }
    res = client.patch(
        "/employee/confirm_account",
        json= confirm_entry
    )
    assert token is not None
    assert res.status_code == 200
    assert res.json() == {'msg': 'account confirmed', 'status_code': 200}



# -------------------- /employee/edit_employee -------------------------

# deepcopy() cuz the dict have nested stuff
edit_employee_entry = copy.deepcopy(data)
edit_employee_entry.pop("email")
edit_employee_entry.pop("number")
edit_employee_entry["roles"].append("VENDOR")

def test_edit_employee(test_db):

    client.post(
        "/employee/add_employee",
        json= data
    )
    response = client.patch(
        "/employee/edit_employee/1",
        json= edit_employee_entry,
    )
    assert response.status_code == 200
    assert response.json() == {'msg': 'employee data updated', 'status_code': '200'}


def test_edit_employee_non_existing_emp(test_db):
    response = client.patch(
        "/employee/edit_employee/5",
        json= edit_employee_entry,
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "employee doesn't exist"}



# -------------------- /employee/get_all_employees -------------------------
def test_get_all_employees(test_db):
    #TODO: add a fixture or sth to fix adding emp & sending mail each req that needs data
    client.post(
        "/employee/add_employee",
        json= data
    )
    res = client.get(
        "/employee/get_all_employees/?skip=0&limit=100"
    )
    assert res.status_code == 200
    assert res.json()["total_records"] == 1
    assert res.json()["employees"][0]["id"] == 1