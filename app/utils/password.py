import re
from fastapi import HTTPException
from pwdlib import PasswordHash
from app import utils


password_hash = PasswordHash.recommended()

def verify_plain_password(password: str, confirm_password):
    password_regex = r'^[a-zA-Z0-9]+$'
    if password is None or confirm_password is None:
        return "password or confirm password is missing!"
    if not re.match(password_regex, password):
        return "password shouldn't contain special caracters!"
    if password != confirm_password:
        return "password does not match!"
    if len(password)<8:
        return "password too short!"
    if len(password)>10:
        return "password too long!"
    return None


def verify_hashed_password(plain_password, hashed_password):
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))


def get_password_hash(password):
    return password_hash.hash(password)