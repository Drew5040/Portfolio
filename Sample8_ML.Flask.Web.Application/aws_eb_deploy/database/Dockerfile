# Get image
FROM postgres:16.1

# Copy schemas and data into docker init to create tables & data
COPY ./schemas/site_content_tables.sql /docker-entrypoint-initdb.d/01-site_content_tables.sql
COPY ./seeds/site_content_insert.sql /docker-entrypoint-initdb.d/02-site_content_insert.sql

# Set locale
RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Service port of PSQL
EXPOSE 5432

# Set default command
CMD ["postgres"]