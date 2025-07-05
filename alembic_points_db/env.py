import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from app.db.base_classes import Base
from app.core.configs import settings
from alembic import context
from app.db.models import (Category, CheckList, Client, Employee, EmployeeShift, Item, Order, Product, ProductOrder,
                           RecipeItem, Shift, StoreItem, Supplier, Supply)


def get_url() -> str:
    db_name = os.environ.get("TARGET_DB_NAME")
    if not db_name:
        db_name = "test_db"
    return settings.data_base.get_db_url(db_name)

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()