import typer
from fulus_cli.cli import users, categories, transactions

app = typer.Typer()
app.add_typer(users.app, name="users", help= "Show all 'users' sub-commands")
app.add_typer(categories.app, name="categories", help= "Show all 'categories' sub-commands")
app.add_typer(transactions.app, name="transactions", help= "Show all 'transactions' sub-commands")