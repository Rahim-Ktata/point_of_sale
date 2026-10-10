from app.models import Employee, AccountActivation
from sqlalchemy.orm import Session


def update_employee_password(db:Session, employee_id=int, password=AccountActivation.password):
    db.query(Employee).filter(Employee.id == employee_id).update(
        {Employee.password: password}, synchronize_session=False
    )
    db.commit()