"""
Module docstring: This module contains the configuration settings for the Flask application,
using environment variables to ensure security and flexibility.
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
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    RATELIMIT_DEFAULT = '100 per minute'

    # Logging & exceptions
    LOGGING_LEVEL = 'DEBUG'
    PROPAGATE_EXCEPTIONS = False

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    POSTGRES_DB = getenv('POSTGRES_DB')
    POSTGRES_USER = getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')



