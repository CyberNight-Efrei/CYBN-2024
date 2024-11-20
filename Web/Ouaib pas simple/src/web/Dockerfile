FROM php:8.2-apache

RUN apt-get update -y && \
    apt-get install -y libpq-dev mariadb-server && \
    docker-php-ext-install pdo pdo_mysql mysqli

COPY ./src/ /var/www/html/

RUN service mariadb start && \
    mariadb -e "CREATE USER 'ouaib'@'localhost' IDENTIFIED BY '17fde36f61af5886617d9e9a68e800e6';" && \
    mariadb -e "CREATE DATABASE ouaib;" && \
    mariadb -e "GRANT ALL PRIVILEGES ON ouaib.* TO 'ouaib'@'localhost';" && \
    mariadb -e "FLUSH PRIVILEGES;"

COPY ./db/ouaib_localhost-2024_11_20_19_10_58-dump.sql /docker-entrypoint-initdb.d/

RUN service mariadb start && \
    mariadb -u root ouaib --force < /docker-entrypoint-initdb.d/ouaib_localhost-2024_11_20_19_10_58-dump.sql

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

RUN echo "CYBN{XSS_g03s_LPE_g03s_RCE_g03s_st0nks}" > /flag

EXPOSE 80

CMD service mariadb start && apache2-foreground
