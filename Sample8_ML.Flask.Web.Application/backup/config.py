from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = getenv('SECRET_KEY', 'disco_king')
    EMAIL_USERNAME = getenv("EMAIL_USERNAME")
    WEB_APP_SECRET = getenv("WEB_APP_SECRET")
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    WTF_CSRF_ENABLED = True
    RATELIMIT_DEFAULT = '50'
    LOGGING_LEVEL = 'INFO'
    PROPAGATE_EXCEPTIONS = False
