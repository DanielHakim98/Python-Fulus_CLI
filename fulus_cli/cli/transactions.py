"""CLI commands for 'Transactions'"""
import datetime
import typer
import re
from config import Config
from fulus_cli import ERRORS
from fulus_cli.sql_orm import db, models
from fulus_cli.sql_orm.models import convert_to_datetime as to_dt

app = typer.Typer()
database = db.DBConnection(Config.SQLALCHEMY_DATABASE_URI)


def _validate_date(date: str) -> datetime.datetime:
    date_datetime, status_code = to_dt(date)
    if status_code != 0:
        typer.secho(
            f"Date does not conform to the expected format.", fg=typer.colors.RED
        )
        raise typer.Exit(1)
    return date_datetime


def _validate_amount(amount: str) -> str:
    if not re.fullmatch(r"^(?:[1-9]\d*|0)(?:\.\d+)?$", amount):
        typer.secho(
            "Amount must be either more than zero and a number", fg=typer.colors.RED
        )
        raise typer.Exit(1)
    return amount


def _category_id(category: str) -> int:
    category_list, status_code = database.get_id(models.Category(title=category))
    if status_code != 0:
        typer.secho(
            f"Category can't be retrieved. Error: {ERRORS.get(status_code)}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    elif len(category_list) < 1:
        typer.secho(f"Category does not exist", fg=typer.colors.RED)
        raise typer.Exit(1)
    return category_list[0].id


def _user_id(user: str) -> int:
    user_list, status_code = database.get_id(models.User(name=user, email=""))
    if status_code != 0:
        typer.secho(
            f"User can't be retrieved. Error: {ERRORS.get(status_code)}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    elif len(user_list) < 1:
        typer.secho(f"User does not exist", fg=typer.colors.RED)
        raise typer.Exit(1)
    return user_list[0].id


@app.command()
def create(
    date: str = typer.Argument(
        ..., help="The date spent (in 'YY-MM-DD' format)", callback=_validate_date
    ),
    amount: str = typer.Argument(
        ..., help="Money spent in currenciless unit", callback=_validate_amount
    ),
    category: str = typer.Argument(..., help="Category name", callback=_category_id),
    user: str = typer.Argument(..., help="User name", callback=_user_id),
):
    """Insert a transaction"""

    transaction = models.Transaction(
        date=date, amount=float(amount), category_id=category, user_id=user
    )

    status_code = database.create(transaction)
    if status_code != 0:
        typer.secho(
            f"Transaction insertion failed. Error {ERRORS[status_code]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Transaction has been inserted.", fg=typer.colors.GREEN)


@app.command()
def delete(tx_id: str = typer.Argument(..., help="The name of the category")):
    """Remove existing transaction"""
    status_code = database.delete(models.Transaction, tx_id)
    if status_code != 0:
        typer.secho(
            f"Transaction can't be removed. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"Transaction ID '{tx_id}' has been removed", fg=typer.colors.GREEN)


@app.command()
def list():
    """List all transactions"""
    result, status_code = database.read(models.Transaction)
    if status_code != 0:
        typer.secho(
            f"Failed while retriveing users. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho("--------------------------------------------")
        typer.secho("id | date | amount | category_id | user_id | ")
        typer.secho("--------------------------------------------")
        for row in result:
            typer.secho(
                " | ".join(
                    [
                        str(row.id),
                        row.date.strftime("%Y-%m-%d"),
                        str(row.amount),
                        str(row.category_id),
                        str(row.user_id),
                    ]
                )
            )


if __name__ == "__main__":
    app()
