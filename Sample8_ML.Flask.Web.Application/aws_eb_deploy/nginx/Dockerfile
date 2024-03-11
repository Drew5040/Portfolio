# Use official Nginx image
FROM nginx:latest

# Create the healthd log directory
RUN mkdir -p /var/log/nginx/healthd/ && \
    chown nginx:nginx /var/log/nginx/healthd/ && \
    chmod 755 /var/log/nginx/healthd/

# Install system dependencies
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Copy the custom configuration file from the current directory to the container
COPY nginx.conf /etc/nginx/nginx.conf


# Expose ports
EXPOSE 80