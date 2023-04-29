import pytest
from unittest.mock import Mock, patch
from config import Config
from typer.testing import CliRunner
from financial_manager import (
    cli,
    __app_name__,
    __version__,
    models
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

class TestUser:
    def test_create_user(self):
        USERNAME = "Daniel"
        EMAIL = "daniel@example.com"
        db_path = Config.SQLALCHEMY_DATABASE_URI

        mocked_create_user = Mock(return_value=0)
        result = runner.invoke(
            cli.app,
            ["create-user", USERNAME, EMAIL]
        )
        with patch('financial_manager.database.create_user', mocked_create_user):
            result = runner.invoke(
                cli.app,
                ["create-user", USERNAME, EMAIL],
                env={"SQLALCHEMY_DATABASE_URI": db_path}
            )
        assert result.exit_code == 0
        assert f"User '{USERNAME}' has been created" in result.stdout
        mocked_create_user.assert_called_once_with(db_path,USERNAME,EMAIL)

    def test_remove_user(self):
        USERNAME = "Daniel"
        EMAIL = "daniel@example.com"
        db_path = Config.SQLALCHEMY_DATABASE_URI

        mocked_remove_user = Mock(return_value=0)
        result = runner.invoke(
            cli.app,
            ["remove-user", USERNAME, EMAIL]
        )
        with patch('financial_manager.database.remove_user', mocked_remove_user):
            result = runner.invoke(
                cli.app,
                ["remove-user", USERNAME, EMAIL],
                env={"SQLALCHEMY_DATABASE_URI": db_path}
            )
        assert result.exit_code == 0
        assert f"User '{USERNAME}' has been removed" in result.stdout
        mocked_remove_user.assert_called_once_with(db_path,USERNAME,EMAIL)

    def test_list_users(self):
        db_path = Config.SQLALCHEMY_DATABASE_URI
        fake_data = [
            models.User(name="Alice", email="alice@example.com"),
            models.User(name="Bob", email="bob@example.com")
        ]
        mock_list_users = Mock(return_value=(fake_data, 0,))

        with patch('financial_manager.database.list_users', mock_list_users):
            result = runner.invoke(cli.app, ['list-users'])

        mock_list_users.assert_called_once_with(db_path)
        expected_output = "------------------\n" \
                        "id | name | email\n" \
                        "------------------\n" \
                        "None | Alice | alice@example.com\n" \
                        "None | Bob | bob@example.com"
        assert result.output.strip() == expected_output