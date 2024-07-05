#!/bin/bash

# Log rotation for alternatives.log
cat <<EOL > /etc/logrotate.d/alternatives
/var/log/alternatives.log {
    monthly
    rotate 12
    compress
    missingok
    notifempty
    create 644 root root
}
EOL

# Log rotation for alternatives.log
cat <<EOL > /etc/logrotate.d/apt
/var/log/apt/*.log {
    monthly
    rotate 12
    compress
    missingok
    notifempty
    create 644 root root
}
EOL

# Log rotation for btmp
cat <<EOL > /etc/logrotate.d/btmp
/var/log/btmp {
    monthly
    rotate 1
    compress
    missingok
    notifempty
    create 600 root utmp
}
EOL

# Log rotation for alternatives.log
cat <<EOL > /etc/logrotate.d/dpkg
/var/log/dpkg.log {
    monthly
    rotate 12
    compress
    missingok
    notifempty
    create 644 root root
}
EOL


# Log rotation for faillog
cat <<EOL > /etc/logrotate.d/faillog
/var/log/faillog {
    monthly
    rotate 12
    compress
    missingok
    notifempty
    create 644 root root
}
EOL

# Log rotation for lastlog
cat <<EOL > /etc/logrotate.d/lastlog
/var/log/lastlog {
    monthly
    rotate 12
    compress
    missingok
    notifempty
    create 644 root root
}
EOL

# Log rotation for Redis logs
cat <<EOL > /etc/logrotate.d/redis
/var/log/redis/*.log {
    daily
    rotate 7
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

# Log rotation for supervisor
cat <<EOL > /etc/logrotate.d/supervisor
/var/log/supervisor/*.log {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    create 644 root root
}
EOL



# Log rotation for wtmp
cat <<EOL > /etc/logrotate.d/wtmp
/var/log/wtmp {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    create 644 root root
}
EOL



