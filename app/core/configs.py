import logging
import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Run(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080

class Logging(BaseModel):
    logging.basicConfig(
        level= logging.INFO,
        format="%(levelname)-9s %(asctime)s - %(module)-15s - %(message)s",
    )

class DataBase(BaseModel):
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "myuser")
    DB_PASS: str = os.getenv("DB_PASS", "mypassword")
    DB_NAME: str = os.getenv("DB_NAME", "mydb")
    DB_AVAILABLE: bool = os.getenv("DB_AVAILABLE", "true").lower() == "true"

    @property
    def sqlalchemy_url(self) -> str:
        url = f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # url = f"postgresql+psycopg2://postgres:J7I1)iuig0mTuq@/postgres?host=/cloudsql/cafemanager-458516:us-central1:cafe-manager-db"
        # url = f"postgresql+psycopg2://postgres:J7I1)iuig0mTuq@34.9.92.218:5432/postgres"
        return url

class JWTToken(BaseModel):
    SECRET_KEY:str = "your-super-secret-key"
    ALGORITHM:str = "HS256"


class Settings(BaseSettings):
    logging: Logging = Logging()
    run: Run = Run()
    data_base: DataBase = DataBase()
    jwt_token: JWTToken = JWTToken()

settings = Settings()