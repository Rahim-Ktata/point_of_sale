

from sqlalchemy import Column, Integer, String, Enum, DateTime, Date, func, CheckConstraint
from ..database import Base


class Error(Base):
    __tablename__ = "error"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, server_default=func.now())

