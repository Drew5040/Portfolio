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
    SECRET_KEY = getenv('SECRET_KEY', 'disco_king')
    EMAIL_USERNAME = getenv("EMAIL_USERNAME")
    WEB_APP_SECRET = getenv("WEB_APP_SECRET")
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    WTF_CSRF_ENABLED = True
    RATELIMIT_DEFAULT = '50'
    LOGGING_LEVEL = 'INFO'
    PROPAGATE_EXCEPTIONS = False
