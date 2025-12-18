from typing import List
# from app.domain import Portfolio
# from app.domain import Transaction
#from app.database import Base
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.db import db

class User(db.Model):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(String(30), primary_key = True)
    password: Mapped[str] = mapped_column(String(100), nullable = False)
    firstname: Mapped[str] = mapped_column(String(50), nullable = False)
    lastname: Mapped[str] = mapped_column(String(50), nullable = False)
    balance: Mapped[float] = mapped_column(Float, nullable = False)
    
    portfolios: Mapped[List["Portfolio"]] = db.relationship("Portfolio", back_populates="user")
    transactions: Mapped[List["Transaction"]] = db.relationship("Transaction", back_populates="user")


    def __str__(self) -> str:
        return(
            f"User(username='{self.username}', "
            f"firstname='{self.firstname} {self.lastname}', "
            f"balance={self.balance})"
        )