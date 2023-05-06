import sqlalchemy as sql
from sqlalchemy import select, delete, Sequence
from sqlalchemy.orm import Session
from fulus_cli import SUCCESS, DB_WRITE_ERR, DB_READ_ERR
from fulus_cli.sql_orm import models

class DBConnection():
    def __init__(self, db_path):
        self.engine = sql.create_engine(db_path)
        self.session = Session(self.engine)

    def get_id(self, model_obj)\
            -> tuple[Sequence[models.Base] | None, int]:
        if isinstance(model_obj, models.User):
            stmt = select(models.User)\
                .where(
                    models.User.name == model_obj.name
                ).where(
                    models.User.email == model_obj.email
                )
        elif isinstance(model_obj, models.Category):
            stmt = select(models.Category).where(
                models.Category.title == model_obj.title
            )

        try:
            with self.session as session:
                result = session.scalars(stmt).all()
            return result, 0
        except Exception as e:
            return None, DB_READ_ERR

    def create(self, model_obj: models.Base) -> int:
        try:
            with self.session as session:
                session.add(model_obj)
                session.commit()
            return SUCCESS
        except Exception as e:
            return DB_WRITE_ERR

    def read(self, model_obj) -> tuple[Sequence[models.Base] | None, int]:
        try:
            with self.session as session:
                result = session.scalars(select(model_obj)).all()
            return result, 0
        except Exception as e:
            return None,DB_READ_ERR

    def delete(self, model_obj, id) -> int:
        try:
            stmt = delete(model_obj).where(model_obj.id == id)
            with self.session as session:
                session.execute(stmt)
                session.commit()
            return SUCCESS
        except Exception as e:
            return DB_WRITE_ERR

    def update(self, model_obj) -> int:
        try:
            with self.session as session:
                session.merge(model_obj)
                session.commit()
            return SUCCESS
        except Exception as e:
            return DB_WRITE_ERR

def init_database(db_path: str) -> int:
    """Create a new financial manager database """
    try:
        engine = sql.create_engine(db_path)
        models.Base.metadata.create_all(engine)
        return SUCCESS
    except Exception as e:
        return DB_WRITE_ERR

def create_category(db_path: str, title: str) -> int:
    pass

def list_categories(
        db_path: str) -> tuple[Sequence[models.Category] | None, int]:
    pass

def delete_category(db_path: str,  title: str) -> int:
    pass