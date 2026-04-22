import os
from src.app.core.config import Settings
def construct_postgresql_url(settings: Settings):
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return database_url
    postgresql_dsn = (
f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}"
        f"/{settings.db_name}"
    )
    return postgresql_dsn
