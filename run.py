import os
from pathlib import Path
import logging
import uvicorn
from app.core.configs import settings
from alembic import command
from alembic.config import Config


def run_alembic_upgrade():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.data_base.sqlalchemy_url)
    command.upgrade(alembic_cfg, "head")
    command.current(alembic_cfg, verbose=True)

def run():
    try:
        if settings.data_base.DB_AVAILABLE:
            run_alembic_upgrade()
        uvicorn.run("app.main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    run()
