import pytest
from config import Config
from fulus_cli.cli import main
from typer.testing import CliRunner
from unittest.mock import Mock, patch
from fulus_cli.sql_orm import db, models
from fulus_cli import (
    DB_WRITE_ERR,
    ERRORS,
    __app_name__,
    __version__
)

runner = CliRunner()

class TestCategory:
    TITLE = 'category_1'
    db_path = Config.SQLALCHEMY_DATABASE_URI

    def test_create_category(self):
        def mocked_create(mocked_self,mocked_obj):
            return 0
        with patch.object(db.DBConnection, 'create', mocked_create):
            result = runner.invoke(
                main.app,
                ["categories","create", TestCategory.TITLE],
                env={"SQLALCHEMY_DATABASE_URI": TestCategory.db_path}
        )
        assert result.exit_code == 0
        assert f"Category '{TestCategory.TITLE}' has been added" \
            in result.stdout

    def test_is_not_empty_title(self):
       TITLE = ""
       result = runner.invoke(
           main.app,
           ["categories","create", TITLE],
        )
       assert result.exit_code == 1
       assert f"Title cannot be empty" in result.stdout

    def test_list_category(self, monkeypatch):
        def mocked_get_all(self, model_obj):
            fake_data = [
                models.Category(title="Transport"),
                models.Category(title="Food"),
                models.Category(title="Saving")
            ]
            return fake_data, 0
        monkeypatch.setattr(db.DBConnection, 'get_all', mocked_get_all)
        result = runner.invoke(
            main.app,
            ["categories", "list"]
        )
        expected_output = "------------\n" \
                "id | title \n" \
                "------------\n" \
                "None | Transport\n" \
                "None | Food\n"\
                "None | Saving"
        assert result.output.strip() == expected_output

    def test_remove_category(self):
        mocked_remove_category = Mock(return_value=0)

        with patch(
                'fulus_cli.sql_orm.db.delete_category',
                mocked_remove_category):
            result = runner.invoke(
                main.app,
                ["categories", "delete", TestCategory.TITLE],
                env={"SQLALCHEMY_DATABASE_URI": TestCategory.db_path}
            )

        assert result.exit_code == 0
        assert f"Category '{TestCategory.TITLE}' has been removed" in result.stdout
        mocked_remove_category.assert_called_once_with(
            TestCategory.db_path,
            TestCategory.TITLE)