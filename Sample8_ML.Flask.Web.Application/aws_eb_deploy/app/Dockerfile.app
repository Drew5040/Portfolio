# Get image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy local project files to container
COPY . .

RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y python3-dev pkg-config libcairo2-dev && \
    apt-get install -y supervisor && \
    apt-get install -y curl && \
    apt-get install -y wget && \
    apt-get install -y redis-tools && \
    apt-get install -y logrotate && \
    apt-get clean && \
    mkdir -p /usr/local/bin && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install memory_profiler objgraph && \
    pip install --no-cache-dir -r requirements.txt

COPY ./.platform/hooks/postdeploy/app-logrotate.sh /usr/local/bin/app-logrotate.sh

# Change permissions for script
RUN chmod 755 /usr/local/bin/app-logrotate.sh

EXPOSE 5000

# Start gunicorn with specified workers, bind address, and configuration file
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
