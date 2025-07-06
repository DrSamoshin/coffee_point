from dotenv import load_dotenv
load_dotenv()

import logging
import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Run(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    ADMIN_MODE: bool = os.getenv("ADMIN_MODE", "false").lower() == "true"

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
    # google proxy connection
    USE_CLOUD_SQL_PROXY: bool = os.getenv("USE_CLOUD_SQL_PROXY", "false").lower() == "true"
    INSTANCE_CONNECTION_NAME: str = os.getenv("INSTANCE_CONNECTION_NAME")
    # local connection
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS") # should be without special symbols

    def get_db_url(self, db_name: str) -> str:
        if self.USE_CLOUD_SQL_PROXY:
            return (f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@/{db_name}"
                   f"?host=/cloudsql/{self.INSTANCE_CONNECTION_NAME}")
        else:
            return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{db_name}"


class JWTToken(BaseModel):
    JWT_SECRET_KEY:str = os.getenv("JWT_SECRET_KEY")
    ALGORITHM:str = "HS256"

class GoogleAccount(BaseModel):
    type: str = "service_account"
    project_id: str = "coffee-point-crm"
    private_key_id: str = os.getenv("PRIVATE_KEY_ID")
    private_key: str = os.getenv("PRIVATE_KEY").replace('\\n', '\n')
    client_email: str = "sa-500@coffee-point-crm.iam.gserviceaccount.com"
    client_id: str = "106356604246273884054"
    auth_uri: str = "https://accounts.google.com/o/oauth2/auth"
    token_uri: str = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url: str = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url: str = "https://www.googleapis.com/robot/v1/metadata/x509/1011837808330-compute%40developer.gserviceaccount.com"
    universe_domain: str = "googleapis.com"

class Settings(BaseSettings):
    logging: Logging = Logging()
    run: Run = Run()
    app_data: AppData = AppData()
    data_base: DataBase = DataBase()
    jwt_token: JWTToken = JWTToken()
    google_account:GoogleAccount = GoogleAccount()

settings = Settings()