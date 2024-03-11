FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3-dev nginx && \
    rm -rf /var/lib/apt/lists/*

# Update pip
RUN pip install --upgrade pip

# Copy project files to container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Configure Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Create directories for server and framework logs
RUN mkdir -p /app/logs/gunicorn /app/logs/flask /var/log/nginx

# Create the files for logs
RUN touch /app/logs/gunicorn/access.log \
          /app/logs/gunicorn/error.log \
          /app/logs/flask/error.log \
          /var/log/nginx/access.log \
          /var/log/nginx/error.log

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py
ENV FLASK_ENV=deployment

# Expose the port Nginx is reachable on
EXPOSE 80
EXPOSE 443
EXPOSE 5000

# Start script to run Gunicorn and Nginx
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]


