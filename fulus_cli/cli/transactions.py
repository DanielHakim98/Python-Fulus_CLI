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

@app.command()
def create(
    date: str = typer.Argument(..., help="date"),
    amount: str = typer.Argument(..., help="amount"),
    category: str = typer.Argument(..., help="category"),
    user: str = typer.Argument(..., help="user"),
):
    """Insert a transaction"""

    date_datetime, status_code = to_dt(date)
    if status_code != 0:
        typer.secho(
            f"Date does not conform to the expected format.",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    # print("date_datetime: ", date_datetime)

    category_data, status_code = database.get_id(models.Category(title=category))
    if status_code != 0:
        typer.secho(
            f"Category can't be retrieved. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    elif len(category_data) < 1:
        typer.secho(
            "Category does not exist",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    category_id = category_data[0].id
    # print("category_data: ", category_data)

    user_data, status_code = database.get_id(models.User(name=user, email=""))
    if status_code != 0:
        typer.secho(
            f"User can't be retrieved. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    elif len(user) < 1:
        typer.secho(
            "User does not exist",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    user_id = user_data[0].id
    # print("user_data: ", user_data)

    transaction = models.Transaction(
        date=date_datetime,
        amount=float(amount),
        category_id=category_id,
        user_id=user_id
    )

    status_code = database.create(transaction)
    if status_code != 0:
        typer.secho(
            f"Transaction insertion failed. Error {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"Transaction has been inserted.",
            fg=typer.colors.GREEN
        )

@app.command()
def delete():
    pass

@app.command()
def list():
    """List all transactions"""
    result, status_code = database.read(
        models.Transaction
    )
    if status_code != 0:
        typer.secho(
            f"Failed while retriveing users. Error: {ERRORS[status_code]}",
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho("--------------------------------------------")
        typer.secho("id | date | amount | category_id | user_id | ")
        typer.secho("--------------------------------------------")
        for row in result:
            typer.secho(' | '.join(
                [
                    str(row.id),
                    row.date.strftime('%Y-%m-%d'),
                    str(row.amount),
                    str(row.category_id),
                    str(row.user_id)
                ]
            ))

if __name__ == "__main__":
    app()