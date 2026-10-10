import re

def verifyPassword(password: str, confirm_password):
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
