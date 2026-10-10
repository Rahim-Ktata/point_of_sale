
from sqlalchemy import Column, Integer, ForeignKey, Enum
from ..database import Base
from app.enums import Role


class EmployeeRole(Base):
    __tablename__ = "employee_role"

    id = Column(Integer, primary_key=True, nullable=False)
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    role = Column(Enum(Role), nullable=False)
