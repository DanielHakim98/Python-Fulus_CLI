""" Financial Manager entry point script."""
from fulus_cli import __app_name__, cli_main

def main():
    cli_main.app(prog_name=__app_name__)

if __name__ == '__main__':
    main()