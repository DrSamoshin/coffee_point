import logging

import uvicorn
from app.core.configs import settings
from alembic import command
from alembic.config import Config
from app.db.session import check_db_availability


def run_alembic_upgrade():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.data_base.sqlalchemy_url)
    command.upgrade(alembic_cfg, "head")
    command.current(alembic_cfg, verbose=True)

def run():
    check_db_availability()
    logging.info("check DB")
    try:
        uvicorn.run("app.main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
    except Exception as error:
        print(error)

    if settings.data_base.DB_AVAILABLE:
        run_alembic_upgrade()
        logging.info("alembic migration was applied")

if __name__ == "__main__":
    run()

