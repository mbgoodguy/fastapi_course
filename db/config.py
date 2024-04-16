import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict

env_path = Path(__file__).parent.parent
load_dotenv(dotenv_path=env_path / '.test.env')


class DB_Settings:
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    MODE: str = os.getenv('MODE')

    DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


settings = DB_Settings()

# print(env_path / '.test.env')
