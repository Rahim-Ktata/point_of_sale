from fastapi import BackgroundTasks, FastAPI

from datetime import datetime
import re
import uuid

from fastapi import FastAPI, Depends, status, HTTPException
from app import emailUtil, schemas, enums, models, database, crud, utils
from sqlmodel import Field, Session, create_engine, select

from app.enums.tokenStatus import TokenStatus

def get_session():
    with Session(database.engine) as session:
        yield session
app = FastAPI()


email_regex = r'^[A-Za-z0-9\.]+@[\w]+\.[\w]+$'
cnss_regex = r'^\d{8}-\d{2}$'
phone_number_regex = r'^\+216\d{8}$'

# front checking is done with conditions below
options = [
    schemas.MatchyOption(display_value="first_name", value="first_name", mandatory=True, type=enums.FieldType.string, conditions=[]),
    schemas.MatchyOption(display_value="last_name", value="last_name", mandatory=True, type=enums.FieldType.string, conditions=[]),
    schemas.MatchyOption(display_value="email", value="email", mandatory=True, type=enums.FieldType.string, conditions=[
        schemas.MatchyCondition(property=enums.ConditonProperty.regex, comparer=enums.Comparer.e, value=email_regex, custom_fail_message="invalid email!")
    ]),
    schemas.MatchyOption(display_value="number", value="number", mandatory=True, type=enums.FieldType.integer, conditions=[]),
    #TODO: add birth_date validation
    schemas.MatchyOption(display_value="birth_date", value="birth_date", mandatory=False, type=enums.FieldType.string, conditions=[]),
    schemas.MatchyOption(display_value="address", value="address", mandatory=False, type=enums.FieldType.string, conditions=[]),
    schemas.MatchyOption(display_value="cnss_number", value="cnss_number", mandatory=False, type=enums.FieldType.string, conditions=[
        schemas.MatchyCondition(property=enums.ConditonProperty.regex, comparer=enums.Comparer.e, value=cnss_regex, custom_fail_message="invalid cnss number!")
    ]),
    schemas.MatchyOption(display_value="contract_type", value="contract_type", mandatory=True, type=enums.FieldType.string, conditions=[
        schemas.MatchyCondition(property=enums.ConditonProperty.val, comparer=enums.Comparer.inn, value=enums.ContractType.getPossibleValues(), custom_fail_message="invalid contract type!")
    ]),
    schemas.MatchyOption(display_value="gender", value="gender", mandatory=True, type=enums.FieldType.string, conditions=[
        schemas.MatchyCondition(property=enums.ConditonProperty.val, comparer=enums.Comparer.inn, value=enums.Gender.getPossibleValues(), custom_fail_message=f"gender must be in: { ", ".join(enums.Gender.getPossibleValues()) }")
    ]),
    schemas.MatchyOption(display_value="phone_number", value="phone_number", mandatory=False, type=enums.FieldType.string, conditions=[
        schemas.MatchyCondition(property=enums.ConditonProperty.regex, comparer=enums.Comparer.e, value=phone_number_regex, custom_fail_message="invalid phone_number!")
    ]),
    schemas.MatchyOption(display_value="roles", value="roles", mandatory=True, type=enums.FieldType.string, conditions=[]),
]

# back fields checking

def is_regex_matched(pattern,field):
    return field if re.match(pattern, field) else None

def is_valid_mail(employee, field):
    return is_regex_matched(email_regex,field)

def is_valid_cnss_number(employee,field):
    contract_type = employee["contract_type"]
    if(contract_type in ['CDI', 'CDD']):
        if is_regex_matched(cnss_regex, field):
            return field
    elif field:
        if is_regex_matched(cnss_regex, field):
            return field
    else: return None


def is_positive_int(employee, field: str):
    # .isdigit don't work here
    # "²".isdigit()   # True
    # int("²")        # ValueError!
    # "١٢٣".isdigit() # True
    try:
        res = int(field)
    except Exception as e:
        return None
    return res
    # return res >= 0

def is_valid_birth_date(employee, date_text):
    format = "%Y-%m-%d"
    res = True
    try:
        res = bool(datetime.strptime(date_text, format))
    except ValueError:
        return None
    return date_text

def is_valid_phone_number(employee, field):
    return is_regex_matched(phone_number_regex,field)

def are_valid_roles(employee, field):
    roles_list = field.split(',')
    for role in roles_list:
        if not enums.Role.isValidEnumValue(role):
            return None
    return field



# def cnss_number_err_msg(employee, field):
#     contract_type = employee["contract_type"]
#     if(contract_type in ['CDI', 'CDD']):
#         if field == None :
#             err_msg = "cnss_number shoudl be provided when contract_type is CDI or CDD"
#     if contract_type and is_regex_matched(cnss_regex, field)==None:
#         err_msg = "cnss number format: xxxxxxxx-xx"
#     return err_msg

fields_check = {
    # field to validate: (func to validate, err msg)
    "email": (lambda employee,field: is_valid_mail(employee,field), "wrong mail address"),
    "gender": (lambda employee,field: enums.Gender.isValidEnumValue(field), f"gender must be in { enums.Gender.getPossibleValues() }"),
    "contract_type": (lambda employee,field: enums.ContractType.isValidEnumValue(field), f"contract_type must be in { enums.ContractType.getPossibleValues() }"),
    # if cnss_number is empty with contract type in cdi cdd it'll be handled without calling this func
    "cnss_number": (lambda employee,field: is_valid_cnss_number(employee,field),f"cnss number should follow the format: xxxxxxxx-xx"),
    "number": (lambda employee,field: is_positive_int(employee,field), "number should be a positive integer"),
    "birth_date": (lambda employee,field: is_valid_birth_date(employee,field), "birth_date should have the format YYYY-MM-DD"),
    "roles": (lambda employee,field: are_valid_roles(employee,field), f"roles should be in { enums.Role.getPossibleValues() }"),
    "phone_number": (lambda employee,field: is_valid_phone_number(employee,field),"phone number must start with +216 followed by 8 digits"),
}


mandatory_fields = {
    "first_name": "First Name",
    "last_name": "Last Name",
    "email": "Email",
    "number": "Number",
    "contract_type": "Contract Type",
    "gender": "Gender",
    "roles": "Roles"
}
optional_fields = {
    "birth_date": "Birth Date",
    "address": "Address",
    "phone_number": "Phone Number",
}
mandatory_with_condition_fields = {
    "cnss_number": "CNSS number"
}
unique_fields = {
    "phone_number": models.Employee.phone_number,
    "email": models.Employee.email
}
possible_fields = {
    **mandatory_fields,
    **optional_fields,
    **mandatory_with_condition_fields
}


def validate_employee_data(employee):
    errs = []
    warnings = []
    # TODO:wrong cells not used, just a feat to be added
    wrong_cells = []
    employee_data = { field: cell.value for field, cell in employee.items() }

    for field in possible_fields:
        # field not included (missing col)
        # we already did this in main.py before calling this func , redundant
        # TODO: delete one of the checks , either this or the one in main
        if field not in employee_data:
            if field in mandatory_fields or (field == "cnss_number" and employee['contract_type'].value in ['CDI','CDD']):
                if(field=="cnss_number"):
                    errs.append(f"line { employee[field].rowIndex }: { possible_fields[field] } is required when Contract type is CDI or CDD")
                else:
                    errs.append(f"line { employee[field].rowIndex }: { possible_fields[field] } is a required field")
                wrong_cells.append({employee[field]['rowIndex'], employee[field]['colIndex']})

        # field included with empty val
        elif employee_data[field] == '':
            if field in mandatory_fields or (field == "cnss_number" and employee['contract_type'].value in ['CDI','CDD']):
                if(field=="cnss_number"):
                    errs.append(f"line { employee[field].rowIndex }: { possible_fields[field] } is required when Contract type is CDI or CDD")
                else:
                    errs.append(f"line { employee[field].rowIndex }: { possible_fields[field] } is a required field")
                wrong_cells.append({employee[field].rowIndex, employee[field].colIndex})
            else:
                employee_data[field] = None # added None in db
        # field exist
        else:
            # if it has condition
            if field in fields_check:
                # condition not satisfied
                # converted (the val in lower upper.. or none if err)
                converted_field = fields_check[field][0](employee_data, employee_data[field]) 
                if converted_field is None:
                    # mandatory field
                    if field in mandatory_fields or (field == "cnss_number" and employee['contract_type'].value in ['CDI','CDD']):
                        errs.append(f"line { employee[field].rowIndex } in { possible_fields[field]}: { fields_check[field][1] } ")
                        wrong_cells.append({employee[field].rowIndex, employee[field].colIndex})
                    else:
                        warnings.append(f"line { employee[field].rowIndex } in { possible_fields[field]}: { fields_check[field][1] } ")
                        wrong_cells.append({employee[field].rowIndex, employee[field].colIndex})
                # condition satisfied
                else:
                    # we might make it lower | upper case
                    employee_data[field] = converted_field

    #TODO: add the wrong cells feat
    return (errs, warnings, employee_data)


# MatchyUploadEntry looks like this:
# {
#     "lines":
#         [
#             {
#                 "first_name":{
#                     "value":"Rahim",
#                     "rowIndex":0,
#                     "colIndex":0
#                 }
#             },
#             {
#                 "first_name":{
#                     "value":"Rahim",
#                     "rowIndex":0,
#                     "colIndex":0
#                 }
#             }
#         ]
# }


def validate_employees_data_and_upload(employees: list, force_upload: bool, background_tasks: BackgroundTasks, db: Session = Depends(get_session)):
    errs = []
    warnings = []
    employees_to_add = []
    roles_per_email = {}
    for employee in employees:
        emp_errs, emp_warnings, emp_data = validate_employee_data(employee)
        errs.extend(emp_errs)
        warnings.extend(emp_warnings)
        roles_per_email[emp_data.get('email')] = emp_data.get('roles').split(',')
        emp_data.pop("roles")
        employees_to_add.append(models.Employee(**emp_data))



    # mail | phone.. exist already in db | given twice
    for field in unique_fields:
        vals = set()
        # enumerate : adds index number (0 based) (to add the line number)
        for line, employee in enumerate(employees):
            val = employee[field].value.strip()
            # empty val
            if val == '':
                continue
            # check duplicate vals for unique fields (from the user input)
            elif val in vals:
                msg = f"line {line}: { field } must be unique, but it exists more than once in the file"
                (errs if field in mandatory_fields else warnings).append(msg)
            else: vals.add(val)

        # check duplicate exist in db
        try:
            # select * from employee where email in ("rahiim@gmail.com", "xy@gmail.com");
            duplicates = db.query(models.Employee).filter(unique_fields[field].in_(vals)).all()
        except Exception as e:
            crud.add_error(db=db,text=str(e))
            raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

        if duplicates :
            used=[]
            for dup in duplicates:
                used.append(getattr(dup,field))
            msg = f"{ (', ').join(used) } already used"
            # we re working in mandatory fields
            # (errs if field in mandatory_fields else warnings).append(msg)
            errs.append(msg)



    if errs or (warnings and not force_upload):
        return schemas.EmployeeUploadResponse(
            errs = errs,
            warnings = warnings
        )
    # else if warnings

    try:
        # --------------- add all to db --------------------------
        db.add_all(employees_to_add)
        db.flush()
        # ---------------- adding roles --------------------------
        employees_roles_to_add = []
        for emp in employees_to_add:
            for role in roles_per_email[emp.email]:
                employees_roles_to_add.append(models.EmployeeRole(employee_id=emp.id, role=role.strip().upper()))
        db.add_all(employees_roles_to_add)
        # db.commit()

        #----------- store a token -------------------------
        tokens_to_add = []
        for emp in employees_to_add:
            db_token = models.AccountActivation(
                employee_id = emp.id,
                email = emp.email,
                token = uuid.uuid1(),
                status = TokenStatus.PENDING
            )
            tokens_to_add.append(db_token)
        db.add_all(tokens_to_add)
        #------------ send mail -----------------------------------
        #------------ we need each employees data for the mail ----
        employees_mails = {}
        for emp in employees_to_add:
            employees_mails[emp.email] = emp.__dict__

        for token in tokens_to_add:
            background_tasks.add_task(emailUtil.simple_send,[token.email], {**employees_mails[token.email],'token':token.token})

        db.commit()

    except Exception as e:
        db.rollback()
        crud.add_error(db=db,text=str(e))
        raise HTTPException(status_code=500, detail=utils.get_err_msg(str(e)))

    return schemas.EmployeeUploadResponse(
        detail="file uploaded successfully",
        status_code=201
    )


