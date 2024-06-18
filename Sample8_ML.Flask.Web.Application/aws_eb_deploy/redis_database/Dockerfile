FROM redis:latest

# Update OS, install OS libraries, change permissions, and create needed directories
RUN apt-get update && \
    apt-get install -y curl wget redis-tools procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/redis/redis-data/ \
             /app/redis/dump-rdb/ \
             /app/redis/redis-config/ \
             /app/redis/log/ && \
    touch /app/redis/log/redis-server.log && \
    chown -R redis:redis /app/redis

# Copy the redis.conf, redis.acl, and custom sysctl.conf files to the container
COPY ./redis-config/redis.conf /app/redis/redis-config/redis.conf
COPY ./redis-config/redis.acl /app/redis/redis-config/redis.acl
COPY ./redis-config/sysctl.conf /etc/sysctl.conf

# Start Redis server with the configuration file
CMD ["redis-server", "/app/redis/redis-config/redis.conf"]


