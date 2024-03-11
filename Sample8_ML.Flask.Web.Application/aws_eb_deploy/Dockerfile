FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies & supervisor to manage servers
RUN apt-get update && \
    apt-get install -y python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Update pip
RUN pip install --upgrade pip

# Copy project files to container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for server and framework logs
RUN mkdir -p /app/logs/gunicorn /app/logs/flask

EXPOSE 5000

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py
ENV FLASK_ENV=deployment

# Start gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]







