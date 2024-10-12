FROM ubuntu:22.04

# Install cron and dependencies
RUN apt-get update && \
    apt-get install -y \
    cron \
    tzdata \
    jq \
    curl && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /etc/cron.*/*

# Create necessary directories
RUN mkdir -p /etc/nginx/modsecurity/aws_ips && \
    chmod -R 755 /etc/nginx/modsecurity/aws_ips

# Copy the update script and ensure it's executable
COPY aws_update_ips.sh /usr/local/bin/aws_update_ips.sh
RUN chmod +x /usr/local/bin/aws_update_ips.sh

# Copy the cron job file (ensure it's using correct crontab format)
COPY aws_update.cron /etc/cron.d/aws_update.cron
RUN chmod 644 /etc/cron.d/aws_update.cron && crontab /etc/cron.d/aws_update.cron

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Dump the environment so cron jobs can access environment variables
RUN printenv >> /etc/environment

# Set the entrypoint to the entrypoint.sh script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Start cron in the foreground and redirect logs to Docker logs
CMD ["cron", "-f", "-l", "2"]
