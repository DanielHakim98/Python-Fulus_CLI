import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite+pysqlite:///" + os.path.join(basedir, "..", "financial_manager.db")


print(Config.SQLALCHEMY_DATABASE_URI)
