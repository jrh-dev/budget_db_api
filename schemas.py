"""
Schema definitions
"""

from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, Integer, String, Boolean, Date, Float
from database import Base

class Config:
    orm_mode = True

class Transaction(BaseModel):
    """
    Pydantic model for Transaction.
    """
    id: int
    incoming: bool = False
    name: str
    seed_date: date
    end_after: int = 0
    value: float = 0
    paid_into: str
    one_off: bool = False
    custom_days: int
    avoid_special_days: bool = False

class SQLATransaction(Base):
    """
    SQLAlchemy model for Transaction.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    incoming = Column(Boolean, default=False)
    name = Column(String, nullable=False)
    seed_date = Column(Date, nullable=False)
    end_after = Column(Integer, default=0)
    value = Column(Float, default=0.0)
    paid_into = Column(String, nullable=False)
    one_off = Column(Boolean, default=False)
    custom_days = Column(Integer, default=0)
    avoid_special_days = Column(Boolean, default=False)