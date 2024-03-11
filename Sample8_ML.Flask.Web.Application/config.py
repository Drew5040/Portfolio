
class Config:
    SECRET_KEY = 'WhosGotAllThisBalls'
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    WTF_CSRF_ENABLED = True
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    LOGGING_LEVEL = 'INFO'
    PROPAGATE_EXCEPTIONS = False