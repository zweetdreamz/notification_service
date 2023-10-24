from dotenv import load_dotenv
import os

from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    HOST = '127.0.0.1'
    PORT = os.environ.get('PORT')
    TEST_EMAIL = os.environ.get('EMAIL')
    DB_URI = os.environ.get('DB_URI')
    REDIS_URI = os.environ.get('REDIS_URI')

    SMTP_HOST = os.environ.get('SMTP_HOST')
    SMTP_PORT = os.environ.get('SMTP_PORT')
    SMTP_LOGIN = os.environ.get('SMTP_LOGIN')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
    SMTP_NAME = os.environ.get('SMTP_NAME')

    API_PREFIX = '/api'

    DB_NAME = 'my_database'
    DB_COLLECTION = 'notifications'


settings = Settings()
