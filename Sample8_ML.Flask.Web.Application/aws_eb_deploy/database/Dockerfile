# Get image
FROM postgres:16.1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl wget && \
    apt-get install -y logrotate && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy schemas and data into docker init to create tables & data
COPY ./schemas/site_content_tables.sql /docker-entrypoint-initdb.d/01-site_content_tables.sql
COPY ./seeds/site_content_insert.sql /docker-entrypoint-initdb.d/02-site_content_insert.sql
COPY ./.platform/hooks/postdeploy/psql-logrotate.sh /usr/local/bin/psql-logrotate.sh

# Change the permissions and ownership of logrotate script
RUN chmod +x /usr/local/bin/psql-logrotate.sh && \
    chown root:root /usr/local/bin/psql-logrotate.sh && \
    chmod 755 /usr/local/bin/psql-logrotate.sh

# Set locale
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Set default command
CMD ["postgres"]
