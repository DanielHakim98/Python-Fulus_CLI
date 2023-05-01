""" Financial Manager entry point script."""
from fulus_cli import __app_name__
from fulus_cli.cli import app

def main():
    app(prog_name=__app_name__)

if __name__ == '__main__':
    main()