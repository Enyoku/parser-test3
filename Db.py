from sqlalchemy import create_engine
from local_settings import posrtgesql as settings

# ?=======================================IF USES PostgreSQL=============================================================

postgr_engine = create_engine(
    f'postgresql+psycopg2://{settings["username"]}:{settings["password"]}@{settings["host"]}/{settings["database"]}', echo=True,)

# ?========================================IF USES SQLite================================================================

sqlite_engine = create_engine('sqlite:///places.sqlite', echo=True)

# ?======================================================================================================================
