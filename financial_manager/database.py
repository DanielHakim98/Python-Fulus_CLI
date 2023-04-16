import sqlalchemy as sql
from financial_manager import models, SUCCESS, DB_WRITE_ERR

def init_database(db_path: str) -> int:
    """Create a new financial manager database """
    try:
        engine = sql.create_engine(db_path)
        models.Base.metadata.create_all(engine)
        return SUCCESS
    except OSError as e:
        return DB_WRITE_ERR

