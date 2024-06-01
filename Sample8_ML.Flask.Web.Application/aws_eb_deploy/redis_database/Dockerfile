FROM redis:latest

WORKDIR /app

# Update OS
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

# Make appropriate log & mount directories
RUN mkdir -p /app/redis/redis-data/ \
             /app/redis/dump-rdb/ \
             /app/redis/redis-config/  \
             /app/redis/log/ && \
    touch    /app/redis/log/redis-server.log && \
    chown -R redis:redis /app/redis

# Copy the redis.conf file to container
COPY redis.conf /app/redis/redis-config/redis.conf
COPY redis.acl  /app/redis/redis-config/redis.acl

ENV REDIS_CONFIG_FILE /app/redis/redis-config/redis.conf
ENV REDIS_ACL_FILE /app/redis/redis-config/redis.acl

CMD ["sh", "-c", "exec redis-server \"$REDIS_CONFIG_FILE\" --aclfile \"$REDIS_ACL_FILE\" --requirepass \"$SUPER_SECRET_PASSWORD\" --bind 0.0.0.0"]





