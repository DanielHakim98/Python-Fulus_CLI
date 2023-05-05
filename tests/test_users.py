import pytest
from config import Config
from fulus_cli.cli import main
from typer.testing import CliRunner
from unittest.mock import patch
from fulus_cli.sql_orm import db, models
from fulus_cli import (
    __app_name__,
    __version__
)

runner = CliRunner()

class TestUser:
    USERNAME = "Daniel"
    EMAIL = "daniel@example.com"
    db_path = Config.SQLALCHEMY_DATABASE_URI

    def test_create_user(self,monkeypatch):
        def mocked_create(mocked_self,mocked_obj):
            return 0
        monkeypatch.setattr(db.DBConnection, 'create', mocked_create)
        result = runner.invoke(
            main.app,
            ["users","create", TestUser.USERNAME, TestUser.EMAIL],
            env={"SQLALCHEMY_DATABASE_URI": TestUser.db_path}
        )
        assert result.exit_code == 0
        assert f"User '{TestUser.USERNAME}' has been created" in result.stdout

    def test_is_not_empty_name(self):
       NAME = ""
       result = runner.invoke(
           main.app,
           ["users","create", NAME, TestUser.EMAIL],
        )
       assert result.exit_code == 1
       assert f"Username or Email cannot be empty" in result.stdout

    def test_valid_email(self):
        EMAIL = "example"
        result = runner.invoke(
           main.app,
           ["users","create", TestUser.USERNAME, EMAIL],
        )
        assert result.exit_code == 1
        assert f"Email must be a valid email address" in result.stdout

    def test_remove_user(self, monkeypatch):
        def mocked_delete(self, model_obj, id):
            return 0
        monkeypatch.setattr(db.DBConnection, "delete", mocked_delete)
        result = runner.invoke(
            main.app,
            ["users", "delete", TestUser.USERNAME, TestUser.EMAIL],
            env={"SQLALCHEMY_DATABASE_URI": TestUser.db_path}
        )
        assert result.exit_code == 0
        assert f"User '{TestUser.USERNAME}' has been removed" in result.stdout

    def test_list_users(self, monkeypatch):
        def mocked_get_all(self, model_obj):
            fake_data = [
                models.User(name="Alice", email="alice@example.com"),
                models.User(name="Bob", email="bob@example.com")
            ]
            return fake_data, 0
        monkeypatch.setattr(db.DBConnection, 'get_all', mocked_get_all)
        result = runner.invoke(main.app, ['users', "list"])
        expected_output = "------------------\n" \
                        "id | name | email\n" \
                        "------------------\n" \
                        "None | Alice | alice@example.com\n" \
                        "None | Bob | bob@example.com"
        assert result.output.strip() == expected_output