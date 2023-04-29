import pytest
from unittest.mock import Mock, patch
from config import Config
from typer.testing import CliRunner
from financial_manager import (
    cli,
    __app_name__,
    __version__
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

def test_create_user():
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

def test_remove_user():
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

def test_list_users():
    db_path = Config.SQLALCHEMY_DATABASE_URI
    mocked_list_users = Mock(return_value=0)
    with patch("financial_manager.database.list_users", mocked_list_users):
        result = runner.invoke(
            cli.app,
            ["list-users"],
            env={"SQLALCHEMY_DATABASE_URI":db_path}
        )
    assert result.exit_code == 0
    mocked_list_users.assert_called_once_with(db_path)