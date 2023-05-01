import pytest
from unittest.mock import Mock, patch
from config import Config
from typer.testing import CliRunner
from fulus_cli import (
    __app_name__,
    __version__,
    cli_main,
    models
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli_main.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
