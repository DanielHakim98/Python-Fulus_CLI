from datetime import datetime
import pytest
from config import Config
from unittest import mock
from fulus_cli.cli import main
from typer.testing import CliRunner
from fulus_cli.sql_orm import db, models

runner = CliRunner()

class TestTransaction:
    date = "2023-05-23"
    amount = "100"
    category= "TestCategory"
    user = "TestUser"
    db_path = Config.SQLALCHEMY_DATABASE_URI

    @pytest.fixture
    def mocked_dbconnection(self, monkeypatch):
        class MockedDBConnection:
            def get_id(self, obj):
                return 100, 0

            def create(self, obj):
                return 0

        mocked_connection = MockedDBConnection()
        monkeypatch.setattr(db.DBConnection, "get_id", mocked_connection.get_id)
        monkeypatch.setattr(db.DBConnection, "create", mocked_connection.create)
        yield mocked_connection

    def test_create_transaction(self, mocked_dbconnection, monkeypatch):
        mocked_to_dt = mock.Mock(
            return_value=(
                datetime.strptime(TestTransaction.date, '%Y-%m-%d'),
                0
            )
        )
        monkeypatch.setattr(models, "convert_to_datetime", mocked_to_dt)

        result = runner.invoke(
            main.app,
            [
                "transactions", "create",
                TestTransaction.date,
                TestTransaction.amount,
                TestTransaction.category,
                TestTransaction.user,
            ],
            env={"SQLALCHEMY_DATABASE_URI": TestTransaction.db_path}
        )

        print("Exit code:", result.exit_code)
        print("Result stdout:", result.stdout)

        assert result.exit_code == 0
        assert "Transaction has been inserted." in result.stdout
        assert mocked_to_dt.called
        assert mocked_dbconnection.get_id.called
        assert mocked_dbconnection.create.called


    def test_list_transaction(self, monkeypatch):
        def mocked_get_all(self, model_object):
            fake_data = [
                models.Transaction(
                    date=datetime(2020, 2, 2),
                    amount=100,
                    category_id=1,
                    user_id=1
                ),
                models.Transaction(
                    date=datetime(2021, 9, 1),
                    amount=9.9,
                    category_id=2,
                    user_id=1
                ),
                models.Transaction(
                    date=datetime(2023, 3, 13),
                    amount=1000,
                    category_id=3,
                    user_id=2
                )
            ]
            return fake_data, 0
        monkeypatch.setattr(db.DBConnection, 'read', mocked_get_all)
        result =runner.invoke(
            main.app,
            ["transactions", "list"]
        )
        expected_output = "--------------------------------------------\n" \
                "id | date | amount | category_id | user_id | \n" \
                "--------------------------------------------\n" \
                "None | 2020-02-02 | 100 | 1 | 1\n" \
                "None | 2021-09-01 | 9.9 | 2 | 1\n"\
                "None | 2023-03-13 | 1000 | 3 | 2"
        assert result.output.strip() == expected_output

    def test_remove_transaction(self, monkeypatch):
        pass

