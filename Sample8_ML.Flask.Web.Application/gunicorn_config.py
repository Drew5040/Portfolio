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

# Specify the Flask application to be run by Gunicorn
chdir = '/app'  # Change to your app directory

# Access log configuration
capture_output = True

accesslog = "/app/logs/gunicorn/access.log"

errorlog = "/app/logs/gunicorn/error.log"

access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

daemon = False  # Set to True if running in daemon mode

raw_env = [
    'FLASK_APP=app.py',  # Specify your main Flask application file
    'FLASK_ENV=production',  # Set the environment to production
]

# Specify the Flask application to be run by Gunicorn
default_proc_name = 'app:FlaskApplication'
