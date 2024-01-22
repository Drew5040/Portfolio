# Number of worker processes
workers = 4

# Host and port to bind to
bind = '0.0.0.0:5000'

# Worker timeout
timeout = 30

# Load application code before forking worker processes
preload = True

# Limit number of requests a worker will process before being restarted gracefully
max_requests = 1000

# Access log configuration
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
