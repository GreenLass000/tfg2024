from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class IncomeList(Base):
    """
    Model representing the IncomeList table in the database.
    """
    __tablename__ = 'incomelist'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    def __repr__(self):
        return f"<IncomeList {self.name}>"
