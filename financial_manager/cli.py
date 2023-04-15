import typer
from typing import Optional
from financial_manager import __app_name__, __version__

app = typer.Typer()


@app.command()
def _version_callback(value: bool) -> None:
    if value:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(version: Optional[bool] = typer.Option(
    None,
    "--version",
    "-v",
    help="Show the application's version and exit.",
    callback=_version_callback, is_eager=True
)) -> None:
    return