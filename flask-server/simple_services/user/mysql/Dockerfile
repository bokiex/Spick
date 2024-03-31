FROM mysql:latest

ENV MYSQL_DATABASE=user \
    MYSQL_ROOT_PASSWORD=password

ADD user.sql /docker-entrypoint-initdb.d

EXPOSE 3306