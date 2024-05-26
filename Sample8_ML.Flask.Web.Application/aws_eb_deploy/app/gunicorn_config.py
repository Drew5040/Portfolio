"""
Gunicorn configuration file for setting various options for the server.
"""

from os import getenv
from app import logger


# Number of worker processes
WORKERS = 4

# Host and port to bind to
PORT = getenv('PORT', '5000')
BIND = f'0.0.0.0:{PORT}'

# Worker timeout
TIMEOUT = 120

# Load application code before forking worker processes
PRELOAD = True

# Limit number of requests a worker will process before being restarted gracefully
MAX_REQUESTS = 1000

# Specify Flask app to run
CHDIR = '/app'

# Capture output
CAPTURE_OUTPUT = True

# Set logging level
LOGLEVEL = 'INFO'

# Access log path in container
ACCESSLOG = "/app/gunicorn/logs/access.log"

# Error log path in container
ERRORLOG = "/app/gunicorn/logs/error.log"

# Set log format
ACCESS_LOG_FORMAT = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Specify the Flask application to be run by Gunicorn
DEFAULT_PROC_NAME = 'app:app'

# Log that gunicorn configs have been accessed
logger.info('Gunicorn config has been accessed ...')
