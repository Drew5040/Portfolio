FROM python:3.10-slim

# Create project directory
WORKDIR /app

# Copy project files to container
COPY . .

# Update pip
RUN pip install --upgrade pip

# Install build dependencies for numpy
RUN apt-get update && \
    apt-get install -y python3-dev
RUN apt-get update && apt-get install -y nginx
RUN pip install --no-cache-dir -r requirements.txt

# Create directories for server and framework logs
RUN mkdir -p /app/logs/nginx
RUN mkdir -p /app/logs/gunicorn
RUN mkdir /app/logs/flask

# Create the files for logs
RUN touch /app/logs/gunicorn/access.log
RUN touch /app/logs/gunicorn/error.log
RUN touch /app/logs/flask/error.log
RUN touch /app/logs/nginx/error.log

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py
ENV FLASK_ENV=deployment

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

