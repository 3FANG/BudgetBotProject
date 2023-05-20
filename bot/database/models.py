from typing import List
import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from bot.database.base import Base


class Budget(Base):
    __tablename__ = "User"

    codename: Mapped[str] = mapped_column(String(255), primary_key=True)
    daily_limit: Mapped[int]

    def __repr__(self) -> str:
        return f"Budget(codename={self.codename!r}, daily_limit={self.daily_limit!r})"


class Category(Base):
    __tablename__ = "Category"

    codename: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    is_base_expanse: Mapped[bool]
    aliases: Mapped[str]

    expenses: Mapped[List["Expense"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"Category(codename={self.codename!r}, name={self.name!r}, is_base_expense={self.is_base_expanse!r}, aliases={self.aliases!r})"


class Expense(Base):
    __tablename__ = "Expense"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]
    created: Mapped[datetime.datetime]
    category_codename = mapped_column(ForeignKey("Category.codename"))
    raw_text: Mapped[str]

    category: Mapped["Category"] = relationship(back_populates="expense")

    def __repr__(self) -> str:
        return f"Expense(id={self.id!r}, amount={self.amount!r}, created={self.created!r}, category_codename={self.category_codename!r}, raw_text={self.raw_text!r})"
