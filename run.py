import logging
import uvicorn
from dotenv import load_dotenv
from alembic import command
from alembic.config import Config
from app.core.configs import settings
from app.db.session import check_db_availability


def run_alembic_upgrade():
    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", settings.data_base.sqlalchemy_url)
        command.upgrade(alembic_cfg, "head")
        command.current(alembic_cfg, verbose=True)
    except Exception as error:
        logging.warning(error)

def run():
    load_dotenv()
    check_db_availability()
    logging.info("check DB")
    try:
        if settings.data_base.DB_AVAILABLE:
            run_alembic_upgrade()
        uvicorn.run("app.main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
    except Exception as error:
        logging.error(error)

if __name__ == "__main__":
    run()
