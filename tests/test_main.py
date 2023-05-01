import pytest
from unittest.mock import Mock, patch
from config import Config
from typer.testing import CliRunner
from fulus_cli import (
    __app_name__,
    __version__
)
from fulus_cli.cli import main
from fulus_cli.sql_orm import models

runner = CliRunner()

def test_version():
    result = runner.invoke(main.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
