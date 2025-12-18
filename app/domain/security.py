#from app.database import Base
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.db import db
# from app.domain import Investment, Transaction


class Security(db.Model):
    __tablename__ = 'security'

    ticker: Mapped[str] = mapped_column(String(10), primary_key=True)
    issuer: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    investments: Mapped[List["Investment"]] = db.relationship("Investment", back_populates="security")
    transactions: Mapped[List["Transaction"]] = db.relationship("Transaction", back_populates="security")
