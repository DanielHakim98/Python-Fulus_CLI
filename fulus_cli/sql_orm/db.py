import sqlalchemy as sql
from sqlalchemy import select, delete,  Sequence
from sqlalchemy.orm import Session
from fulus_cli import SUCCESS, DB_WRITE_ERR, DB_READ_ERR
from fulus_cli.sql_orm import models

def init_database(db_path: str) -> int:
    """Create a new financial manager database """
    try:
        engine = sql.create_engine(db_path)
        models.Base.metadata.create_all(engine)
        return SUCCESS
    except Exception as e:
        return DB_WRITE_ERR

def create_user(db_path: str, name: str, email: str) -> int:
    """Create a new user from the given name"""
    try:
        engine = sql.create_engine(db_path)
        user = models.User(name=name, email=email)
        with Session(engine) as session:
            session.add(user)
            session.commit()
        return SUCCESS

    except Exception as e:
        return DB_WRITE_ERR

def remove_user(db_path: str, name: str, email: str) -> int:
    """Remove a user from the given name and email"""
    try:
        engine = sql.create_engine(db_path)
        stmt = delete(models.User)\
                .where(models.User.name == name)\
                .where(models.User.email == email)
        with Session(engine) as session:
            session.execute(stmt)
            session.commit()
        return SUCCESS

    except Exception as e:
        return DB_WRITE_ERR

def list_users(db_path: str) -> tuple[Sequence[models.User] | None, int]:
    """Get list of users created"""
    try:
        engine = sql.create_engine(db_path)
        with Session(engine) as session:
            result = session.scalars(select(models.User)).all()
        return result, 0
    except Exception as e:
        return None, DB_READ_ERR

def create_category(db_path: str, title: str) -> int:
    pass

def list_categories(
        db_path: str) -> tuple[Sequence[models.Category] | None, int]:
    pass

def delete_category(db_path: str,  title: str) -> int:
    pass