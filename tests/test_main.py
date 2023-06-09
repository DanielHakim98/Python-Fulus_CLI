import pytest
from typer.testing import CliRunner
from fulus_cli.config import Config
from fulus_cli.cli import main
from fulus_cli.sql_orm import db
from fulus_cli import __app_name__, __version__

runner = CliRunner()


def test_version():
    result = runner.invoke(main.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_init(monkeypatch):
    def mock_init_database(db_path):
        return 0

    monkeypatch.setattr(db, "init_database", mock_init_database)
    # Simulate pressing "Enter"
    monkeypatch.setattr("builtins.input", lambda _: "")

    result = runner.invoke(main.app, ["init"])

    print("Exit code:", result.exit_code)
    print("Result stdout:", result.stdout)
    assert result.exit_code == 0
    assert (
        f"The finance cli database is {Config.SQLALCHEMY_DATABASE_URI}" in result.stdout
    )
