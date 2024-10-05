FROM ubuntu:24.04

# Install cron and dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    cron \
    jq \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /etc/nginx/modsecurity/aws_ips && \
    chmod -R 755 /etc/nginx/modsecurity/aws_ips

# Copy scripts
COPY aws_update_ips.sh /usr/local/bin/aws_update_ips.sh
RUN chmod +x /usr/local/bin/aws_update_ips.sh

# Copy cronjob definition (with .cron extension) to /etc/cron.d/
COPY aws_update.cron /etc/cron.d/aws_update.cron

# Ensure cron job file has correct permissions
RUN chmod 644 /etc/cron.d/aws_update.cron

# Apply the cron job
RUN crontab /etc/cron.d/aws_update.cron

# Start cron service in the foreground
CMD ["cron", "-f"]
