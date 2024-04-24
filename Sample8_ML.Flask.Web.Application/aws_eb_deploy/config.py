"""
config.py

This module contains the configuration settings for the Flask application, using environment variables to ensure
security and flexibility.

"""
from os import getenv


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
    MAX_CONTENT_LENGTH = getenv("MAX_CONTENT_LENGTH")
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
    REDIS_HOST = getenv("REDIS_HOST")
    REDIS_PORT = getenv("REDIS_PORT")
    REDIS_DB = getenv("REDIS_DB")
    SUPER_SECRET_PASSWORD = getenv("SUPER_SECRET_PASSWORD")
