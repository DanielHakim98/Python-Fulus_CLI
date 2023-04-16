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
    Column,
    ForeignKey,
    extract,
)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)

    transactions: Mapped[list["Transaction"] | None] = relationship(back_populates = "user")

    def __init__(self, name: str, email:str) -> None:
        self.name = name
        self.email = email

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"

class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)

    transactions: Mapped[list["Transaction"] | None] = relationship(back_populates = "category")

    def __init__(self, title: str) -> None:
        self.title = title

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, title={self.title!r})"

class Transaction(Base):
    __tablename__ = "transaction"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    amount: Mapped[float ]= mapped_column(Float, default = 0.0)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    category: Mapped[Category] = relationship(back_populates = "transaction")
    user: Mapped[User] = relationship(back_populates = "transaction")

    def __init__(self, date: datetime, amount:float, category_id: int, user_id: int) -> None:
        self.date = date
        self.amount = amount
        self.category_id = category_id
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"Transaction(id={self.id!r}, date={self.date!r}, amount={self.amount!r}, category_id={self.category_id!r}, user_id={self.user_id!r})"
