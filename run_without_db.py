from app.core.configs import settings
from run import run

if __name__ == "__main__":
    settings.data_base.DB_AVAILABLE = False
    run()
    