"""Top-level package for finance_manager"""
__app_name__ = "financial_manager"
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
    DIR_ERR: "Config directory error",
    FILE_ERR: "Config file error",
    DB_READ_ERR: "Database read error",
    DB_WRITE_ERR: "Database write error",
    ID_ERR: "Id error",
}