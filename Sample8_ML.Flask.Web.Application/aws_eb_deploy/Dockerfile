# Get image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get install -y python3-dev pkg-config libcairo2-dev && \
    apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/*

# Update pip
RUN pip install --upgrade pip

# Copy project files to container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose service port
EXPOSE 5000

# Start gunicorn with specified workers, bind address, and configuration file
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
