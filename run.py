import os
from pathlib import Path
import logging
import uvicorn
from app.core.configs import settings
from alembic import command
from alembic.config import Config


BASE_DIR = Path(__file__).resolve().parent
contents = os.listdir(BASE_DIR)

def run_alembic_upgrade():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.data_base.sqlalchemy_url)
    command.upgrade(alembic_cfg, "head")
    logging.info("Checking current migration version...")
    command.current(alembic_cfg, verbose=True)

if __name__ == "__main__":
    try:
        run_alembic_upgrade()
        logging.info("Starting FastAPI")
        logging.info(f"Folder contents %s: %s", BASE_DIR, contents)
        uvicorn.run("app.main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
    except Exception as error:
        print(error)