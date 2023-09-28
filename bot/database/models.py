from typing import List
import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, BIGINT, TIMESTAMP

from bot.database.base import Base


class Users(Base):
    __tablename__ = "Users"

    id: Mapped[BIGINT] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    fisrt_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    signed: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True))

    categories: Mapped[List["Category"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, username={self.username!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, signed={self.signed!r})"


class Category(Base):
    __tablename__ = "Category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))

    user: Mapped["Users"] = relationship(back_populates="categories")
    expenses: Mapped[List["Expense"]] = relationship(back_populates="category")
    aliases: Mapped[List["Aliases"]] = relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"Category(codename={self.codename!r}, name={self.name!r}, is_base_expense={self.is_base_expanse!r}, aliases={self.aliases!r})"


class Expense(Base):
    __tablename__ = "Expense"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int]
    created: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True))
    category_id: Mapped[int] = mapped_column(ForeignKey("Category.id"))
    raw_text: Mapped[str]

    category: Mapped["Category"] = relationship(back_populates="expenses")

    def __repr__(self) -> str:
        return f"Expense(id={self.id!r}, amount={self.amount!r}, created={self.created!r}, category_id={self.category_id!r}, raw_text={self.raw_text!r})"


class Aliases(Base):
    __tablename__ = "Aliases"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("Category.id"))

    category: Mapped["Category"] = relationship(back_populates="aliases")

    def __repr__(self) -> str:
        return f"Aliases(id={self.id!r}, name={self.name!r}, category_id={self.category_id!r})"
