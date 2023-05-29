import pytest
from config import Config
from fulus_cli.cli import main
from typer.testing import CliRunner
from fulus_cli.sql_orm import db, models
from fulus_cli import DB_WRITE_ERR, ERRORS, __app_name__, __version__

runner = CliRunner()


class TestCategory:
    TITLE = "category1"
    db_path = Config.SQLALCHEMY_DATABASE_URI

    def test_create_category(self, monkeypatch):
        def mocked_create(mocked_self, mocked_obj):
            return 0

        monkeypatch.setattr(db.DBConnection, "create", mocked_create)
        result = runner.invoke(
            main.app,
            ["categories", "create", TestCategory.TITLE],
            env={"SQLALCHEMY_DATABASE_URI": TestCategory.db_path},
        )
        assert result.exit_code == 0
        assert f"Category '{TestCategory.TITLE}' has been added" in result.stdout

    def test_is_not_empty_title(self):
        TITLE = ""
        result = runner.invoke(
            main.app,
            ["categories", "create", TITLE],
        )
        assert result.exit_code == 1
        assert f"Name cannot be empty" in result.stdout

    def test_list_category(self, monkeypatch):
        def mocked_get_all(self, model_obj):
            fake_data = [
                models.Category(title="Transport"),
                models.Category(title="Food"),
                models.Category(title="Saving"),
            ]
            return fake_data, 0

        monkeypatch.setattr(db.DBConnection, "read", mocked_get_all)
        result = runner.invoke(main.app, ["categories", "list"])
        expected_output = (
            "------------\n"
            "id | title \n"
            "------------\n"
            "None | Transport\n"
            "None | Food\n"
            "None | Saving"
        )
        assert result.output.strip() == expected_output

    def test_remove_category(self, monkeypatch):
        def mocked_delete(self, model_obj, id):
            return 0

        def mocked_get_id(self, mode_obj):
            return [models.Category(title=TestCategory.TITLE)], 0

        monkeypatch.setattr(db.DBConnection, "delete", mocked_delete)
        monkeypatch.setattr(db.DBConnection, "get_id", mocked_get_id)
        result = runner.invoke(
            main.app,
            ["categories", "delete", TestCategory.TITLE],
            env={"SQLALCHEMY_DATABASE_URI": TestCategory.db_path},
        )

        assert result.exit_code == 0
        assert f"Category '{TestCategory.TITLE}' has been removed" in result.stdout

    def test_update_category(self, monkeypatch):
        category_id = "100"
        title = "NewTitle"

        def mocked_update(self, mocked_obj, id):
            return 0

        monkeypatch.setattr(db.DBConnection, "update", mocked_update)
        result = runner.invoke(
            main.app,
            ["categories", "update", category_id, "--title", title],
            env={"SQLALCHEMY_DATABASE_URI": TestCategory.db_path},
        )
        print("Exit code:", result.exit_code)
        print("Result stdout:", result.stdout)
        assert result.exit_code == 0
        assert f"Category ID '{category_id}' has been updated" in result.stdout
