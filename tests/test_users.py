import pytest
from config import Config
from fulus_cli.cli import main
from typer.testing import CliRunner
from unittest.mock import Mock, patch
from fulus_cli.sql_orm import models
from fulus_cli import (
    DB_WRITE_ERR,
    ERRORS,
    __app_name__,
    __version__
)

runner = CliRunner()

class TestUser:
    USERNAME = "Daniel"
    EMAIL = "daniel@example.com"
    db_path = Config.SQLALCHEMY_DATABASE_URI

    def test_create_user(self):
        mocked_create_user = Mock(return_value=0)
        with patch('fulus_cli.sql_orm.db.create_user', mocked_create_user):
            result = runner.invoke(
                main.app,
                ["users","create", TestUser.USERNAME, TestUser.EMAIL],
                env={"SQLALCHEMY_DATABASE_URI": TestUser.db_path}
            )

        assert result.exit_code == 0
        assert f"User '{TestUser.USERNAME}' has been created" in result.stdout
        mocked_create_user.assert_called_once_with(
            TestUser.db_path,
            TestUser.USERNAME,
            TestUser.EMAIL
        )

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

    def test_remove_user(self):
        mocked_remove_user = Mock(return_value=0)
        with patch('fulus_cli.sql_orm.db.remove_user', mocked_remove_user):
            result = runner.invoke(
                main.app,
                ["users", "delete", TestUser.USERNAME, TestUser.EMAIL],
                env={"SQLALCHEMY_DATABASE_URI": TestUser.db_path}
            )
        assert result.exit_code == 0
        assert f"User '{TestUser.USERNAME}' has been removed" in result.stdout
        mocked_remove_user.assert_called_once_with(
            TestUser.db_path,
            TestUser.USERNAME,
            TestUser.EMAIL)

    def test_list_users(self):
        db_path = Config.SQLALCHEMY_DATABASE_URI
        fake_data = [
            models.User(name="Alice", email="alice@example.com"),
            models.User(name="Bob", email="bob@example.com")
        ]
        mock_list_users = Mock(return_value=(fake_data, 0,))

        with patch('fulus_cli.sql_orm.db.list_users', mock_list_users):
            result = runner.invoke(main.app, ['users', "list"])

        mock_list_users.assert_called_once_with(db_path)
        expected_output = "------------------\n" \
                        "id | name | email\n" \
                        "------------------\n" \
                        "None | Alice | alice@example.com\n" \
                        "None | Bob | bob@example.com"
        assert result.output.strip() == expected_output