import sqlalchemy as sql
from sqlalchemy.orm import Session
from fulus_cli import models, SUCCESS, DB_WRITE_ERR, DB_READ_ERR

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
        query = f"""
            INSERT INTO {models.User.__tablename__} (name, email)
            VALUES (:name, :email)
        """
        with Session(engine) as session:
            session.execute(sql.text(query), [{"name": name, "email": email}])
            session.commit()
        return SUCCESS

    except Exception as e:
        return DB_WRITE_ERR

from sqlalchemy import delete
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

from sqlalchemy import select, Sequence
def list_users(db_path: str) -> tuple[ Sequence[models.User] | None, int ]:
    """Get list of users created"""
    try:
        engine = sql.create_engine(db_path)
        with Session(engine) as session:
            result = session.scalars(select(models.User)).all()
        return result, 0
    except Exception as e:
        return None, DB_READ_ERR
