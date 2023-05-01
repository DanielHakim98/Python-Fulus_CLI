import typer
from fulus_cli.cli import users, categories

app = typer.Typer()
app.add_typer(users.app, name="users")
app.add_typer(categories.app, name="categories")