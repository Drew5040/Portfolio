# Base image with necessary build tools
FROM ubuntu:24.04

# Avoid prompts during installation
ARG DEBIAN_FRONTEND=noninteractive

# Set environment variables for modsecurity
ENV MODSEC_TMP_DIR=/var/modsecurity/tmp
ENV MODSEC_DATA_DIR=/var/modsecurity/data

# Install build tools and dependencies (curl & ping added for debugging)
RUN apt-get update && \
    apt-get install -y \
    nginx \
    curl \
    iputils-ping \
    make \
    automake \
    build-essential \
    zlib1g-dev \
    libpcre3 \
    libpcre3-dev \
    libssl-dev \
    wget \
    git \
    libxml2-dev \
    libyajl-dev \
    libgeoip-dev \
    libtool \
    dh-autoreconf \
    libcurl4-openssl-dev \
    liblmdb-dev \
    pkgconf &&\
    rm -rf /var/lib/apt/lists/*

# Clone and build ModSecurity
RUN git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity.git /opt/modsecurity && \
    cd /opt/modsecurity && \
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make && \
    make install

# Clone ModSecurity-Nginx connector
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git /opt/modsecurity-nginx

# Download, compile and install Nginx with ModSecurity module
RUN NGINX_VERSION=$(nginx -v 2>&1 | grep -o '[0-9]*\.[0-9]*\.[0-9]*') && \
    mkdir -p /opt && \
    wget http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz -O /opt/nginx.tar.gz && \
    cd /opt && \
    tar zxvf nginx.tar.gz && \
    cd nginx-$NGINX_VERSION && \
    ./configure --with-compat --add-dynamic-module=/opt/modsecurity-nginx && \
    make modules && \
    mkdir -p /usr/local/nginx/modules && \
    cp objs/ngx_http_modsecurity_module.so /usr/local/nginx/modules

# Create Nginx user & group
RUN getent group nginx || groupadd -r nginx
RUN getent passwd nginx || useradd -r -g nginx -s /bin/false -d /var/www nginx

# Make all config & logging directories for nginx & modsecurity
RUN mkdir -p $MODSEC_TMP_DIR $MODSEC_DATA_DIR \
            /opt/modsecurity/var/log/ \
            /var/modsecurity/tmp/ \
            /var/modsecurity/data/ \
            /etc/modsecurity/ \
            /etc/nginx/modules-available \
            /etc/nginx/modules-enabled \
            /data/nginx/cache \
            /var/log/nginx/healthd/

# Adjust permissions and ownership
RUN chown -R nginx:nginx $MODSEC_TMP_DIR $MODSEC_DATA_DIR /data/nginx/cache /var/log/nginx/healthd/ && \
    chmod -R 700 $MODSEC_TMP_DIR $MODSEC_DATA_DIR && \
    chmod -R 770 /data/nginx/cache && \
    chmod -R 755 /var/log/nginx/healthd/

# Create needed files
RUN touch /opt/modsecurity/var/log/debug.log \
          /var/log/modsec_audit.log \
          /var/log/nginx/healthd/access.log

# Copy config files from project dir to container
COPY modsecurity/conf/modsecurity.conf /etc/modsecurity/
COPY modsecurity/conf/crs-setup.conf /etc/modsecurity/
COPY modsecurity/rules/ /etc/modsecurity/
COPY conf/nginx.conf /etc/nginx/nginx.conf


# Create symbolic link so Nginx can load ModSecurity
RUN echo "load_module /usr/local/nginx/modules/ngx_http_modsecurity_module.so;" > /etc/nginx/modules-available/modsecurity.conf && \
    ln -s /etc/nginx/modules-available/modsecurity.conf /etc/nginx/modules-enabled/modsecurity.conf

# Expose port 80 so Nginx can route traffic to Gunicorn server
EXPOSE 80

# Spin up Nginx
CMD ["nginx", "-g", "daemon off;"]