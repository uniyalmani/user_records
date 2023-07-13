import os
from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    db_url: str = os.getenv("DB_URL", default=os.getenv("DB_URL", "sqlite:///database.db"))
    secret_key: str = os.getenv("SECRET_KEY", default=os.getenv("SECRET_KEY", "test_db"))
    file_location: str = os.getenv("FILE_LOCATION", default=os.getenv("FILE_LOCATION", os.path.join(os.getcwd(), 'files')))
    class Config:
        env_file = ".env"
