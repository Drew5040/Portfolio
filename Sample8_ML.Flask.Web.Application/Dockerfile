FROM python:3.11.7-slim

WORKDIR /app

# Create directories for logs
RUN mkdir -p /app/logs/gunicorn
RUN mkdir /app/logs/flask

# Create files for logs
RUN touch /app/logs/gunicorn/access.log
RUN touch /app/logs/gunicorn/error.log
RUN touch /app/logs/flask/error.log

# Update pip
RUN pip install --upgrade pip

# Install build dependencies for numpy
RUN apt-get update && \
    apt-get install -y python3-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the FLASK_APP environment variable
ENV FLASK_APP=app.py
ENV FLASK_ENV=deployment

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]


