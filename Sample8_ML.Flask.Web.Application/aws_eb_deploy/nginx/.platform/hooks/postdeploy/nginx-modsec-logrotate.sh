#!/bin/bash

cat <<EOL > /etc/logrotate.d/syslog
/var/log/auth.log
/var/log/syslog
/var/log/kern.log
/var/log/boot.log
/var/log/cron.log
/var/log/daemon.log
/var/log/user.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 640 root adm
    sharedscripts
    postrotate
        /usr/lib/rsyslog/rsyslog-rotate > /dev/null 2>/dev/null || true
    endscript
}
EOL

# Log rotation for alternatives.log
cat <<EOL > /etc/logrotate.d/alternatives-log
/var/log/alternatives.log {
    monthly
    rotate 12
    compress
    missingok
    notifempty
    create 644 root root
}
EOL

# Log rotation for history.log & term.log
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

# Log rotation for bootstrap.log
cat <<EOL > /etc/logrotate.d/bootstrap-log
/var/log/bootstrap.log {
    monthly
    rotate 1
    compress
    missingok
    notifempty
    create 600 root utmp
}
EOL

# Log rotation for btmp log
cat <<EOL > /etc/logrotate.d/btmp-log
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
cat <<EOL > /etc/logrotate.d/dpkg-log
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

# Log rotation for modsec_audit.log
cat <<EOL > /etc/logrotate.d/modsec-audit-log
/var/log/modsec_audit.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 644 nginx adm
    sharedscripts
    postrotate
        /usr/sbin/nginx -s reload > /dev/null 2>/dev/null || true
    endscript
}
EOL

# Log rotation for modsec debug.log
cat <<EOL > /etc/logrotate.d/modsec-debug-log
 /opt/ModSecurity/var/log/debug.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 644 nginx adm
    sharedscripts
    postrotate
        /usr/sbin/nginx -s reload > /dev/null 2>/dev/null || true
    endscript
}
EOL

# Log rotation for nginx error.log
cat <<EOL > /etc/logrotate.d/nginx-error-log
/var/log/nginx/error.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 644 nginx adm
    sharedscripts
    postrotate
        /usr/sbin/nginx -s reload > /dev/null 2>/dev/null || true
    endscript
}
EOL

# Log rotation for nginx access.log
cat <<EOL > /etc/logrotate.d/nginx-access-log
/var/log/nginx/access.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 644 nginx adm
    sharedscripts
    postrotate
        /usr/sbin/nginx -s reload > /dev/null 2>/dev/null || true
    endscript
}
EOL




# Log rotation for ModSecurity tmp files
cat <<EOL > /etc/logrotate.d/modsecurity-tmp
/var/modsecurity/tmp/* {
    daily
    rotate 7
    compress
    missingok
    notifempty
    sharedscripts
    postrotate
        find /var/modsecurity/tmp -type f -mtime +7 -exec rm {} \;
    endscript
}
EOL

# Log rotation for ModSecurity tmp_data files
cat <<EOL > /etc/logrotate.d/modsecurity-tmp-data
/var/modsecurity/tmp_data/* {
    daily
    rotate 7
    compress
    missingok
    notifempty
    sharedscripts
    postrotate
        find /var/modsecurity/tmp_data -type f -mtime +7 -exec rm {} \;
    endscript
}
EOL
