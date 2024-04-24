FROM redis:latest

# Make appropriate log & mount directories
RUN mkdir -p /usr/local/etc/redis/ \
          -p /var/app/redis-data \
          -p /var/app/redis-config \
          -p /var/lib/redis \
          -p /usr/local/etc/redis \
          -p /var/log/redis && \
    touch /var/log/redis/redis-server.log

# Copy the redis.conf file to container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose default port for Redis
EXPOSE 6379

CMD ["sh", "-c", "exec redis-server /usr/local/etc/redis/redis.conf --requirepass \"$SUPER_SECRET_PASSWORD\""]



