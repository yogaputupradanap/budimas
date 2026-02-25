# Stage 1: Build dependencies dengan Composer 2
FROM composer:2 AS build
WORKDIR /var/www/html
COPY . ./
RUN composer install --no-dev --optimize-autoloader

# Stage 2: Production image pakai PHP 7.4
FROM php:7.4-apache

# Install ekstensi PHP yang umum dipakai Laravel
RUN docker-php-ext-install -j"$(nproc)" opcache pdo pdo_mysql

# Konfigurasi PHP untuk Cloud Run
RUN set -ex; \
  { \
    echo "; Cloud Run enforces memory & timeouts"; \
    echo "memory_limit = -1"; \
    echo "max_execution_time = 0"; \
    echo "; File upload at Cloud Run network limit"; \
    echo "upload_max_filesize = 32M"; \
    echo "post_max_size = 32M"; \
    echo "; Configure Opcache for Containers"; \
    echo "opcache.enable = On"; \
    echo "opcache.validate_timestamps = Off"; \
    echo "; Configure Opcache Memory (Application-specific)"; \
    echo "opcache.memory_consumption = 32"; \
  } > "$PHP_INI_DIR/conf.d/cloud-run.ini"

# Copy source code dan vendor dari build stage
WORKDIR /var/www/html
COPY . ./
COPY --from=build /var/www/html/vendor ./vendor

# Enable mod_rewrite (Laravel butuh untuk routing)
RUN a2enmod rewrite

# Permission untuk storage dan cache
RUN chmod -R 777 /var/www/html/storage \
 && chmod -R 777 /var/www/html/bootstrap/cache

# Ganti port 80 ke $PORT (Cloud Run contract)
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

# Pakai php.in
