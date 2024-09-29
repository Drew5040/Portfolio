#!/bin/bash

# Log rotation for Redis logs in Celery container (if redis-tools is used)
cat <<EOL > /etc/logrotate.d/redis
/var/log/redis/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 644 redis redis
    sharedscripts
}
EOL

