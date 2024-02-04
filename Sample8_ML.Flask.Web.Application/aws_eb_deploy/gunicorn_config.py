import os

# Number of worker processes
workers = 4

# Host and port to bind to
bind = '0.0.0.0:{}'.format(os.getenv('PORT', 5000))

# Worker timeout
timeout = 30

# Load application code before forking worker processes
preload = True

# Limit number of requests a worker will process before being restarted gracefully
max_requests = 1000

# Specify Flask app to run
chdir = '/app'

# Capture output
capture_output = True

# Access log path in container
accesslog = "/app/logs/gunicorn/access.log"

# Error log path in container
errorlog = "/app/logs/gunicorn/error.log"

# Set log format
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Set environment variables
raw_env = [
    'FLASK_APP=app.py',
    'FLASK_ENV=production',
]

# Specify the Flask application to be run by Gunicorn
default_proc_name = 'app:FlaskApplication'
