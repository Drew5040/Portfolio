FROM alpine:latest

# Install cron and dependencies
RUN apk add --no-cache bash curl jq cron

# Create necessary directories
RUN mkdir -p /etc/nginx/modsecurity/aws_ips && \
    chmod -R 755 /etc/nginx/modsecurity/aws_ips

# Copy scripts
COPY aws_update_ips.sh /usr/local/bin/aws_update_ips.sh
RUN chmod +x /usr/local/bin/aws_update_ips.sh

# Copy cronjob definition (with .cron extension) to /etc/cron.d/
COPY aws_update_ips.cron /etc/cron.d/aws_update_ips.cron

# Ensure cron job file has correct permissions
RUN chmod 644 /etc/cron.d/aws_update_ips.cron

# Start cron service in the foreground
CMD ["crond", "-f"]
