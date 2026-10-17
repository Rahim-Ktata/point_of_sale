

error_keys = {
    "employee_roles_employee_id_fkey": "No Employee with this id",
    "employee_roles_pkey": "No Employee Role with this id",
    "ck_employees_cnss_number": "Cnss number should be {8 digits}-{2 digits} and it's Mandatory for Cdi and Cdd",
    "employee_email_key": "Email already used",
    "employee_pkey": "No employee with this id",
    "ck_employee_phone_number": "Phone number should be 8 digits",
    "value is not a valid email address": "Invalid email address"
}

def get_err_msg(err_msg):
    for err_key in error_keys:
        if err_key in err_msg:
            return error_keys[err_key]
    return "something went wrong"
