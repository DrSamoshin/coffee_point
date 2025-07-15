from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from app.db.base_classes import BaseUser
from app.core.configs import settings
from alembic import context
from app.db.models import User


def get_url() -> str:
    return settings.data_base.get_db_url("users")


config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseUser.metadata


def run_migrations_online() -> None:
    connectable = create_engine(get_url(), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
