#from app.database import Base
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db
# from app.domain import Portfolio, Security

class Investment(db.Model):
    __tablename__ = 'investment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"), nullable=False)
    ticker: Mapped[str] = mapped_column(ForeignKey("security.ticker"), nullable=False)

    portfolio: Mapped["Portfolio"] = db.relationship("Portfolio", back_populates="investments")
    security: Mapped["Security"] = db.relationship("Security", back_populates="investments")


