import logging
import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Run(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080

class AppData(BaseModel):
    title: str = "Coffee point"
    version: str = "1.0.0"
    openapi_version: str = "3.1.0"
    description: str = "This backend application is built on FastAPI and implements the full logic of cafe management."


class Logging(BaseModel):
    logging.basicConfig(
        level= logging.INFO,
        format="%(levelname)-9s %(asctime)s - %(module)-15s - %(message)s",
    )

class DataBase(BaseModel):
    DB_AVAILABLE: bool = True
    # proxy db connection
    USE_CLOUD_SQL_PROXY: bool = os.getenv("USE_CLOUD_SQL_PROXY", "false").lower() == "true"
    INSTANCE_CONNECTION_NAME: str = os.getenv("INSTANCE_CONNECTION_NAME")
    # IP connection
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    DB_USER: str = os.getenv("DB_USER", "myuser")
    DB_PASS: str = os.getenv("DB_PASS", "mypassword") # should be without special symbols
    DB_NAME: str = os.getenv("DB_NAME", "mydb")

    @property
    def sqlalchemy_url(self) -> str:
        if self.USE_CLOUD_SQL_PROXY:
            return (f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@/{self.DB_NAME}"
                   f"?host=/cloudsql/{self.INSTANCE_CONNECTION_NAME}")
        else:
            return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class JWTToken(BaseModel):
    SECRET_KEY:str = "your-super-secret-key"
    ALGORITHM:str = "HS256"


class Settings(BaseSettings):
    logging: Logging = Logging()
    run: Run = Run()
    app_data: AppData = AppData()
    data_base: DataBase = DataBase()
    jwt_token: JWTToken = JWTToken()

settings = Settings()