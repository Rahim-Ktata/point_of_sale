from fastapi.testclient import TestClient
from app.main import app
from app.tests.conftest import get_emp_account_activation_token, get_emp_reset_password_token
from app.tests.test_employee import data

client = TestClient(app)


# ---------------- /forget_password --------------------
def test_forget_password(test_db):
    client.post(
        "/employee/add_employee",
        json= data
    )
    # ----- confirm acc -------
    token = get_emp_account_activation_token(test_db)
    confirm_entry = {
        "token": token,
        "password": "rahim123",
        "confirm_password": "rahim123"
    }
    client.patch(
        "/employee/confirm_account",
        json= confirm_entry
    )

    response = client.post(
        "/forget_password",
        # we use params= not json=
        params = {
            "email":"abdrrahimktata@gmail.com",
        }
    )
    res = response.json()
    response.status_code == 200
    assert res == {"msg": "email sent successfully","status_code": 200}


def test_forget_password_invalid_mail(test_db):
    response = client.post(
        "/forget_password",
        params = {
            "email":"1",
        }
    )
    res = response.json()
    response.status_code == 404
    assert res == {"detail": "email is not registered!"}


def test_forget_password_inactive_account(test_db):
    # ----- create emp -------
    client.post(
        "/employee/add_employee",
        json= data
    )
    response = client.post(
        "/forget_password",
        params = {
            "email":"abdrrahimktata@gmail.com",
        }
    )
    res = response.json()
    response.status_code == 404
    assert res == {"detail": "The requested account is inactive!"}



# ---------------- /reset_password --------------------
def test_reset_password(test_db):
    # ----- create emp -------
    client.post(
        "/employee/add_employee",
        json= data
    )
    # ----- confirm acc -------
    token = get_emp_account_activation_token(test_db)
    confirm_entry = {
        "token": token,
        "password": "rahim123",
        "confirm_password": "rahim123"
    }
    client.patch(
        "/employee/confirm_account",
        json= confirm_entry
    )

    # ----- store pswd reset token -------
    res = client.post(
        "/forget_password",
        params={"email":"abdrrahimktata@gmail.com"}
    )

    token = get_emp_reset_password_token(test_db)

    # ----- reset pswd -------
    response = client.post(
        "/reset_password",
        json = {
            "token": token,
            "password": "12345678",
            "confirm_password": "12345678"
        }
    )
    res = response.json()
    response.status_code == 200
    assert res == {
        "msg": "Password reset successfully!",
        "status_code": 200
    }

