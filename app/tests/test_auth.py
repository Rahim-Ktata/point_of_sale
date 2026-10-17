from fastapi.testclient import TestClient
from app.main import app
from app.tests.conftest import get_emp_account_activation_token
from app.tests.test_employee import data

client = TestClient(app)


# ---------------- /token --------------------
def test_token(test_db):
    #TODO: optimize this
    response = client.post(
        "/employee/add_employee",
        json= data
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
    response = client.post(
        "/token",
        # we use data= not json= cuz we wanna send as form data
        data = {
            "username":"abdrrahimktata@gmail.com",
            "password":"rahim123"
        }
    )
    res = response.json()
    response.status_code == 200
    assert "access_token" in res
    assert res["token_type"] == "bearer"