"""
config.py

This module contains the configuration settings for the Flask application, using environment variables to ensure
security and flexibility.

"""
from os import getenv
# from dotenv import load_dotenv
#
# paths = [
#     './app_container.env',
#     './celery_queue/celery_container.env',
#     './redis_database/redis_container.env',
#     './nginx/nginx_container.env',
#     './database/psql_container.env',
# ]
#
# for path in paths:
#     load_dotenv(path)


class Config:
    """
   Config class stores configuration variables for the Flask application, loading them
   from environment variables where available, with default values set for development.
   """

    # Flask
    SECRET_KEY = getenv('SECRET_KEY')
    EMAIL_USERNAME = getenv("EMAIL_USERNAME")
    WEB_APP_SECRET = getenv("WEB_APP_SECRET")

    # Network
    SESSION_COOKIE_SECURE = getenv("SESSION_COOKIE_SECURE")
    REMEMBER_COOKIE_SECURE = getenv("REMEMBER_COOKIE_SECURE")
    SESSION_COOKIE_HTTPONLY = getenv("SESSION_COOKIE_HTTPONLY")
    SESSION_COOKIE_SAMESITE = getenv("SESSION_COOKIE_SAMESITE")
    MAX_CONTENT_LENGTH = int(getenv("MAX_CONTENT_LENGTH", "10485760"))
    RATELIMIT_DEFAULT = getenv("RATELIMIT_DEFAULT")

    # Logging & exceptions
    LOGGING_LEVEL = getenv('LOGGING_LEVEL')
    PROPAGATE_EXCEPTIONS = getenv("PROPAGATE_EXCEPTIONS")

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    POSTGRES_DB = getenv('POSTGRES_DB')
    POSTGRES_USER = getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')

    # Redis
    REDIS_USERNAME = getenv("REDIS_USERNAME")
    REDIS_HOST = getenv("REDIS_HOST")
    REDIS_PORT = getenv("REDIS_PORT")
    REDIS_DB = getenv("REDIS_DB")
    SUPER_SECRET_PASSWORD = getenv("SUPER_SECRET_PASSWORD")

    # Celery
    CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
    RESULT_BACKEND = getenv("RESULT_BACKEND")
