import os
from src.app.core.config import Settings

def construct_postgresql_url(settings: Settings):
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return database_url

    if not all([
        settings.db_user,
        settings.db_password,
        settings.db_host,
        settings.db_name
    ]):
        raise ValueError("❌ Database configuration missing")

    return (
        f"postgresql://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
