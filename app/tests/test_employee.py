from fastapi.testclient import TestClient

from app import enums, models
from ..config import settings
from app.main import app
from app.tests.conftest import test_db

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


def get_emp_account_activation_token(test_db):
    return test_db.query(models.AccountActivation).filter(models.AccountActivation.employee_id==1).first().token


def test_add_employee(test_db):
    response = client.post(
        "/employee/add_employee",
        json= data
    )
    assert response.status_code == 200

    res = response.json()
    assert res["created_on"] is not None
    res.pop("created_on")
    assert res == {
        "id": 1,
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


def test_add_employee_wrong_email(test_db):
    data= {
        "first_name": "Rahim",
        "last_name": "ktata",
        "email": "a",
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

    response = client.post(
        "/employee/add_employee",
        json= data
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid email address'}


def test_add_employee_wrong_phone_number(test_db):
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
        "phone_number": "a",
        "roles": [
            "ADMIN","VENDOR"
        ]
    }

    response = client.post(
        "/employee/add_employee",
        json= data
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Phone number should be 8 digits"}


def test_add_employee_wrong_cnss_number(test_db):
    data= {
        "first_name": "Rahim",
        "last_name": "ktata",
        "email": "abdrrahimktata@gmail.com",
        "number": 0,
        "birth_date": "2026-10-15",
        "address": "address",
        "cnss_number":"a",
        "contract_type": "CDI",
        "gender": "MALE",
        "account_status": "INACTIVE",
        "phone_number": "12345678",
        "roles": [
            "ADMIN","VENDOR"
        ]
    }

    response = client.post(
        "/employee/add_employee",
        json= data
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Cnss number should be {8 digits}-{2 digits} and it's Mandatory for Cdi and Cdd"}



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

edited_data= {
    "first_name": "Rahim_edited",
    "last_name": "ktata_edited",
    "birth_date": "2026-10-15",
    "address": "address",
    "cnss_number": "12345678-12",
    "contract_type": "CDI",
    "gender": "MALE",
    "account_status": "ACTIVE",
    "phone_number": "12345678",
    "roles": [
        "VENDOR"
    ]
}

def test_edit_employee(test_db):
    client.post(
        "/employee/add_employee",
        json= data
    )
    response = client.patch(
        "/employee/edit_employee/1",
        json= edited_data,
    )
    assert response.status_code == 200
    assert response.json() == {'msg': 'employee data updated', 'status_code': '200'}


def test_edit_employee_non_existing_emp(test_db):
    response = client.patch(
        "/employee/edit_employee/5",
        json= edited_data,
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "employee doesn't exist"}