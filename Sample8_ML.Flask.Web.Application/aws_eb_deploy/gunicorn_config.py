"""
Gunicorn configuration file for setting various options for the server.
"""

from os import getenv

# Number of worker processes
WORKERS = 4

# Host and port to bind to
PORT = getenv('PORT', '5000')  # Ensure default is string to match getenv expected return type
BIND = f'0.0.0.0:{PORT}'

# Worker timeout
TIMEOUT = 30

# Load application code before forking worker processes
PRELOAD = True

# Limit number of requests a worker will process before being restarted gracefully
MAX_REQUESTS = 1000

# Specify Flask app to run
CHDIR = '/app'

# Capture output
CAPTURE_OUTPUT = True

# Access log path in container
ACCESSLOG = "/app/logs/gunicorn/access.log"

# Error log path in container
ERRORLOG = "/app/logs/gunicorn/error.log"

# Set log format
ACCESS_LOG_FORMAT = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Set environment variables
RAW_ENV = [
    'FLASK_APP=app.py',
    'FLASK_ENV=production',
]

# Specify the Flask application to be run by Gunicorn
DEFAULT_PROC_NAME = 'app:FlaskApplication'
