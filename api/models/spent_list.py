from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base


class SpentList(Base):
    """
    Model representing the SpentList table in the database.
    """
    __tablename__ = 'spentlist'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    isconcertado: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __repr__(self):
        return f"<SpentList {self.name}, isconcertado {self.isconcertado}>"
