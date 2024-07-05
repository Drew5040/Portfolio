FROM redis:latest

WORKDIR /app

# Update OS, install OS libraries, change permissions, and create needed directories
RUN apt-get update && \
    apt-get install -y curl wget redis-tools procps && \
    apt-get install -y logrotate && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /app/redis/dump-rdb/ \
             /app/redis/redis-config/ \
             /app/redis/log/ \
             /usr/local/bin && \
    touch /app/redis/log/redis-server.log


# Copy the redis.conf, redis.acl, and custom sysctl.conf files to the container
COPY ./redis-config/redis.conf /app/redis/redis-config/redis.conf
COPY ./redis-config/redis.acl /app/redis/redis-config/redis.acl
COPY ./redis-config/sysctl.conf /etc/sysctl.conf
COPY ./.platform/hooks/postdeploy/redis-logrotate.sh /usr/local/bin/redis-logrotate.sh

RUN chown -R redis:redis /app/redis && \
    chmod 755 /usr/local/bin/redis-logrotate.sh
 \
    # Start Redis server with the configuration file
CMD ["redis-server", "/app/redis/redis-config/redis.conf"]


