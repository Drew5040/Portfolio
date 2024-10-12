#!/bin/sh

# Dump the current environment to /etc/environment so cron inherits it
env >> /etc/environment

# Start cron in the foreground to keep the container alive
exec "$@"