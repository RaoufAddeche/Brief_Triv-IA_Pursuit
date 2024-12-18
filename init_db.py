import sqlmodel as sm
from sqlalchemy import Engine
from enums import Filenames

def get_engine() -> Engine:
    sqlitefile_name = Filenames.SQLITE_DB.value
    sqlite_url = f"sqlite:///{sqlitefile_name}"
    engine = sm.create_engine(sqlite_url, echo=False)
    return engine