"""Top-level package for fulus_cli"""
__app_name__ = "fulus_cli"
__version__ = "0.10"

(
    SUCCESS,
    DIR_ERR,
    FILE_ERR,
    DB_READ_ERR,
    DB_WRITE_ERR,
    ID_ERR,
) = range(6)

ERRORS = {
    DIR_ERR: "Directory error",
    FILE_ERR: "File error",
    DB_READ_ERR: "Database read error",
    DB_WRITE_ERR: "Database write error",
    ID_ERR: "Id error",
}