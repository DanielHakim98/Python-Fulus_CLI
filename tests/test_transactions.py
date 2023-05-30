import pytest
from datetime import datetime
from fulus_cli.config import Config
from fulus_cli.cli import main, transactions
from typer.testing import CliRunner
from fulus_cli.sql_orm import db, models

runner = CliRunner()


class TestTransaction:
    date = "2023-05-23"
    amount = "100"
    category = "Food"
    user = "Danil"
    db_path = Config.SQLALCHEMY_DATABASE_URI

    def test_create_transaction(self, monkeypatch):
        def mocked_id(self, mocked_obj):
            if isinstance(mocked_obj, models.Category):
                return ([models.Category(title=TestTransaction.category)], 0)
            elif isinstance(mocked_obj, models.User):
                return ([models.User(name=TestTransaction.user, email="")], 0)
            else:
                raise ValueError("Invalid object type")

        def mocked_create(self, mocked_obj):
            return 0

        monkeypatch.setattr(db.DBConnection, "get_id", mocked_id)
        monkeypatch.setattr(db.DBConnection, "create", mocked_create)
        result = runner.invoke(
            main.app,
            [
                "transactions",
                "create",
                TestTransaction.date,
                TestTransaction.amount,
                TestTransaction.category,
                TestTransaction.user,
            ],
            env={"SQLALCHEMY_DATABASE_URI": TestTransaction.db_path},
        )

        print("Exit code:", result.exit_code)
        print("Result stdout:", result.stdout)

        assert result.exit_code == 0
        assert "Transaction has been inserted." in result.stdout

    def test_list_transaction(self, monkeypatch):
        def mocked_get_all(self, model_object):
            fake_data = [
                models.Transaction(
                    date=datetime(2020, 2, 2), amount=100, category_id=1, user_id=1
                ),
                models.Transaction(
                    date=datetime(2021, 9, 1), amount=9.9, category_id=2, user_id=1
                ),
                models.Transaction(
                    date=datetime(2023, 3, 13), amount=1000, category_id=3, user_id=2
                ),
            ]
            return fake_data, 0

        monkeypatch.setattr(db.DBConnection, "read", mocked_get_all)
        result = runner.invoke(main.app, ["transactions", "list"])
        expected_output = (
            "--------------------------------------------\n"
            "id | date | amount | category_id | user_id | \n"
            "--------------------------------------------\n"
            "None | 2020-02-02 | 100 | 1 | 1\n"
            "None | 2021-09-01 | 9.9 | 2 | 1\n"
            "None | 2023-03-13 | 1000 | 3 | 2"
        )
        assert result.output.strip() == expected_output

    def test_remove_transaction(self, monkeypatch):
        tx_id = "100"

        def mocked_delete(self, mocked_obj, id):
            return 0

        monkeypatch.setattr(db.DBConnection, "delete", mocked_delete)
        result = runner.invoke(
            main.app,
            ["transactions", "delete", tx_id],
            env={"SQLALCHEMY_DATABASE_URI": TestTransaction.db_path},
        )
        print("Exit code:", result.exit_code)
        print("Result stdout:", result.stdout)
        assert result.exit_code == 0
        assert f"Transaction ID '{tx_id}' has been removed" in result.stdout

    def test_update_transactions(self, monkeypatch):
        tx_id = "100"
        amount = "1000"

        def mocked_update(self, mocked_obj, id):
            return 0

        monkeypatch.setattr(db.DBConnection, "update", mocked_update)
        result = runner.invoke(
            main.app,
            ["transactions", "update", tx_id, "--amount", amount],
            env={"SQLALCHEMY_DATABASE_URI": TestTransaction.db_path},
        )
        print("Exit code:", result.exit_code)
        print("Result stdout:", result.stdout)
        assert result.exit_code == 0
        assert f"Transaction ID '{tx_id}' has been updated" in result.stdout
