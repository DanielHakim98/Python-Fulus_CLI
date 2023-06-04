import alembic.config
from alembic import command
import sqlalchemy as sql
from sqlalchemy import select, delete, update, exists, Sequence
from sqlalchemy.orm import Session
from fulus_cli import SUCCESS, DB_WRITE_ERR, DB_READ_ERR
from fulus_cli.sql_orm import models


class DBConnection:
    def __init__(self, db_path):
        self.engine = sql.create_engine(db_path)
        self.session = Session(self.engine)

    def get_id(self, model_obj) -> tuple[Sequence[models.Base] | None, int]:
        if isinstance(model_obj, models.User):
            stmt = select(models.User).where(models.User.name == model_obj.name)
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
            return None, DB_READ_ERR

    def delete(self, model_obj, id) -> int:
        try:
            # Validate id exists within databse
            exists_query = select(exists().where(model_obj.id == id))
            result = self.session.execute(exists_query).scalar()
            if bool(result) is False:
                print("Transaction ID does not exist")
                return DB_WRITE_ERR

            stmt = delete(model_obj).where(model_obj.id == id)
            with self.session as session:
                session.execute(stmt)
                session.commit()
            return SUCCESS
        except Exception as e:
            return DB_WRITE_ERR

    def update(self, model_obj, values_with_id: dict[any, any]) -> int:
        try:
            exists_query = select(
                exists().where(model_obj.id == int(values_with_id["id"]))
            )
            result = self.session.execute(exists_query).scalar()
            if bool(result) is False:
                return DB_WRITE_ERR

            stmt = update(model_obj)
            with self.session as session:
                session.execute(
                    stmt,
                    [values_with_id],
                )
                session.commit()
            return SUCCESS

        except Exception as e:
            return DB_WRITE_ERR


def init_database(db_path: str) -> int:
    """Create a new financial manager database"""

    try:
        # Run Alembic migrations
        alembic_cfg = alembic.config.Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", db_path)
        command.upgrade(alembic_cfg, "head")

        return SUCCESS
    except Exception as e:
        return DB_WRITE_ERR
