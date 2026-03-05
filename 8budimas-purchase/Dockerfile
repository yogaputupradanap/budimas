# --- Build Stage with Composer 2 ---
FROM composer:2 as build

WORKDIR /app

# Copy source code to container
COPY . .

# Install dependencies (tanpa prestissimo)
RUN composer install --no-dev --optimize-autoloader


# --- Production Stage with Apache & PHP ---
FROM php:8.0-apache

# Install required PHP extensions
RUN docker-php-ext-install -j"$(nproc)" opcache pdo pdo_mysql

# Configure PHP
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
    echo "opcache.memory_consumption = 32"; \
  } > "$PHP_INI_DIR/conf.d/cloud-run.ini"

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Copy built app (including vendor) from build stage
WORKDIR /var/www/html
COPY --from=build /app ./

# Set permissions
RUN chmod -R 777 /var/www/html/storage/ \
    && chmod -R 777 /var/www/html/bootstrap/cache

# Replace Apache port with Cloud Run's PORT env
RUN sed -i 's/80/${PORT}/g' /etc/apache2/sites-available/000-default.conf /etc/apache2/ports.conf

# Use development php.ini (optional: switch to production for prod)
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
