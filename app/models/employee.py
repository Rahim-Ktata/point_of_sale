
from sqlalchemy import Column, Integer, String, Enum, DateTime, Date, func, CheckConstraint

from app.models.employeeRole import EmployeeRole
from ..database import Base
from app.enums import Gender, ContractType, AccountStatus
from sqlalchemy.orm import relationship



class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    number = Column(Integer, nullable=False)
    birth_date = Column(Date, nullable=True)
    address = Column(String, nullable=True)
    cnss_number = Column(String, nullable=True)
    contract_type = Column(Enum(ContractType), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    account_status = Column(Enum(AccountStatus), nullable=False, default=AccountStatus.INACTIVE)
    phone_number = Column(String, nullable=True)
    created_on = Column(DateTime, nullable=False, server_default=func.now())
    roles =  relationship(EmployeeRole)

    __table_args__ = (
        CheckConstraint(
            "(contract_type IN ('CDI', 'CDD') AND cnss_number IS NOT NULL AND cnss_number ~ '^\\d{8}-\\d{2}$') OR (contract_type IN ('APPRENTI', 'SIVP') AND (cnss_number IS NULL OR cnss_number ~ '^\\d{8}-\\d{2}$'))",
            name='ck_employees_cnss_number'
        ),
        CheckConstraint(
            "phone_number ~ '^\\d{8}$'",
            name='ck_employee_phone_number'
        ),
    )
