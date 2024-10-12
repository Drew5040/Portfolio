#!/bin/bash

# Log rotation for Redis logs in /var/log
cat <<EOL > /etc/logrotate.d/redis
/var/log/redis/*.log {
    daily
    rotate 10
    compress
    missingok
    notifempty
    create 644 redis redis
    sharedscripts
}
EOL

# Log rotation for Redis logs in /app/redis/log
cat <<EOL > /etc/logrotate.d/redis-server
/app/redis/log/redis-server.log {
    daily
    rotate 10
    compress
    missingok
    notifempty
    create 644 redis redis
    sharedscripts
    postrotate
        /usr/local/bin/redis-cli shutdown && /usr/local/bin/redis-server /app/redis/redis-config/redis.conf > /dev/null 2>/dev/null || true
    endscript
}
EOL
