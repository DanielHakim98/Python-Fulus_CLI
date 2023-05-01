import re
from fulus_cli import FILE_ERR
from datetime import datetime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "transaction_user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

    transactions: Mapped[list["Transaction"] | None] = relationship(back_populates="user")

    __table_args__ = (
        UniqueConstraint('name', 'email', name='uq_user_name_email'),\
        UniqueConstraint('name', name='uq_user_name')
    )

    def __init__(self, name: str, email:str) -> None:
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"


class Category(Base):
    __tablename__ = "transaction_category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)

    transactions: Mapped[list["Transaction"] | None] = relationship(back_populates="category")

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, title={self.title!r})"


class Transaction(Base):
    __tablename__ = "transaction_master"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    amount: Mapped[float ]= mapped_column(Float, default = 0.0)
    category_id: Mapped[int] = mapped_column(ForeignKey("transaction_category.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("transaction_user.id"), nullable=False)

    category: Mapped[Category] = relationship(back_populates="transactions")
    user: Mapped[User] = relationship(back_populates="transactions")

    def __init__(self, date: datetime, amount:float, category_id: int, user_id: int) -> None:
        self.date = convert_to_datetime(date)
        self.amount = amount
        self.category_id = category_id
        self.user_id = user_id

    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.id!r}"
            + f"date={self.date!r}"
            + f"amount={self.amount!r}"
            + f"category_id={self.category_id!r}"
            + f"user_id={self.user_id!r})"
        )


def convert_to_datetime(date:str)-> datetime | int:
    pattern = r"^(19\d{2}|20[0-2][0-9])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    if re.match(pattern, date):
        split = date.split('-')
        return datetime(split[0],split[1],split[2])
    return FILE_ERR