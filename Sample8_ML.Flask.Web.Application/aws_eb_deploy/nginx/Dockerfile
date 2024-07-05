# Base image with necessary build tools
FROM ubuntu:24.04

# Avoid prompts during installation
ARG DEBIAN_FRONTEND=noninteractive

# Set NGINX_VERSION and MODSECURITY_COMMIT as environment variables
ARG NGINX_VERSION=1.26.1
ARG MODSECURITY_COMMIT=dc8af8f23d6c23407a5bcb6da7b28a3c025f914b
ARG MODSECURITY_NGINX_COMMIT=ef64996aedd4bb5fa1831631361244813d48b82f

# Install build tools and dependencies (curl & ping added for debugging)
RUN apt-get update && \
    apt-get install -y \
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
    logrotate \
    pkgconf &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone and build ModSecurity
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity.git /opt/ModSecurity && \
    cd /opt/ModSecurity && \
    git checkout $MODSECURITY_COMMIT && \
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make && \
    make install

# Clone ModSecurity-Nginx connector
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git /opt/ModSecurity-nginx && \
    cd /opt/ModSecurity-nginx && \
    git checkout $MODSECURITY_NGINX_COMMIT



# $(nginx -v 2>&1 | grep -o '[0-9]*\.[0-9]*\.[0-9]*')
# Download, compile and install Nginx with ModSecurity module
RUN NGINX_VERSION=1.26.1 && \
    mkdir -p /opt && \
    wget http://nginx.org/download/nginx-$NGINX_VERSION.tar.gz -O /opt/nginx.tar.gz && \
    cd /opt && \
    tar zxvf nginx.tar.gz && \
    cd nginx-$NGINX_VERSION && \
    export CFLAGS="-U_FORTIFY_SOURCE" && \
    ./configure --with-compat --add-dynamic-module=/opt/ModSecurity-nginx \
    --prefix=/etc/nginx \
    --sbin-path=/usr/sbin/nginx \
    --modules-path=/usr/lib/nginx/modules \
    --conf-path=/etc/nginx/nginx.conf \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/run/nginx.lock \
    --http-client-body-temp-path=/var/cache/nginx/client_temp \
    --http-proxy-temp-path=/var/cache/nginx/proxy_temp \
    --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
    --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
    --http-scgi-temp-path=/var/cache/nginx/scgi_temp \
    --user=nginx \
    --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module \
    --with-http_auth_request_module --with-http_dav_module --with-http_flv_module \
    --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module \
    --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module \
    --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module \
    --with-http_v2_module --with-http_v3_module --with-mail --with-mail_ssl_module --with-stream \
    --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module \
    --with-cc-opt='-g -O2 -ffile-prefix-map=/data/builder/debuild/nginx-1.26.1/debian/debuild-base/nginx-1.26.1=. \
                  -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat \
                  -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' \
    --with-ld-opt='-Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie' && \
    make && \
    make install && \
    mkdir -p /usr/local/nginx/modules && \
    cp objs/ngx_http_modsecurity_module.so /usr/local/nginx/modules

# Create Nginx user & group
RUN getent group nginx || groupadd -r nginx
RUN getent passwd nginx || useradd -r -g nginx -s /bin/false -d /var/www nginx

# Make all config & logging directories for nginx & modsecurity
RUN mkdir -p $MODSEC_TMP_DIR $MODSEC_DATA_DIR \
            /opt/ModSecurity/var/log/ \
            /var/modsecurity/tmp/ \
            /var/modsecurity/tmp_data/ \
            /etc/nginx/modsecurity/rules/ \
            /etc/nginx/modsecurity/ \
            /etc/nginx/modules-available \
            /etc/nginx/modules-enabled \
            /var/cache/nginx \
            /var/cache/nginx/client_temp \
            /var/cache/nginx/proxy_temp \
            /var/cache/nginx/fastcgi_temp \
            /var/cache/nginx/uwsgi_temp \
            /var/cache/nginx/scgi_temp \
            /usr/share/nginx/html/static \
            /data/nginx/cache \
            /usr/local/bin

# Copy config files from project dir to container
COPY modsecurity/conf/modsecurity.conf /etc/nginx/modsecurity/
COPY modsecurity/conf/crs-setup.conf /etc/nginx/modsecurity/
COPY modsecurity/rules/* /etc/nginx/modsecurity/rules/
COPY modsecurity/conf/crs-setup.conf /etc/nginx/modsecurity/
COPY modsecurity/conf/main.conf /etc/nginx/modsecurity/
COPY modsecurity/conf/unicode.mapping /etc/nginx/modsecurity/
COPY conf/nginx.conf /etc/nginx/nginx.conf
COPY ./.platform/hooks/postdeploy/nginx-modsec-logrotate.sh /usr/local/bin/nginx-modsec-logrotate.sh

# Change permissions for main.conf and /rules
RUN chmod 644 /etc/nginx/modsecurity/main.conf && \
    chmod -R 755 /etc/nginx/modsecurity/rules && \
    \
    # Change the permissions and ownership of the logrotate script
    chmod +x /usr/local/bin/nginx-modsec-logrotate.sh && \
    chown root:root /usr/local/bin/nginx-modsec-logrotate.sh &&  \
    chmod 755 /usr/local/bin/nginx-modsec-logrotate.sh && \
    \
    # Adjust permissions and ownership
    chown -R nginx:nginx $MODSEC_TMP_DIR $MODSEC_DATA_DIR /var/cache/nginx /usr/share/nginx/html/static && \
    touch /opt/ModSecurity/var/log/debug.log /var/log/modsec_audit.log

# Create symbolic link so Nginx can load ModSecurity
RUN echo "load_module /usr/local/nginx/modules/ngx_http_modsecurity_module.so;" > /etc/nginx/modules-available/modsecurity.conf && \
    ln -s /etc/nginx/modules-available/modsecurity.conf /etc/nginx/modules-enabled/modsecurity.conf

# Expose port 80 so Nginx can route traffic to Gunicorn server
EXPOSE 80

# Spin up Nginx
CMD ["nginx", "-g", "daemon off;"]