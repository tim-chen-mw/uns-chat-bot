from alembic.config import Config
from alembic.command import upgrade
from ..util.settings import DB_URL


def perform_database_migrations():
    """Use alembic to migrade the database if needed"""
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "alembic")
    alembic_cfg.set_main_option("sqlalchemy.url", DB_URL)
    upgrade(alembic_cfg, "head")
