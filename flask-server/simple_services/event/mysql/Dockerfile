FROM mysql:latest

ENV MYSQL_DATABASE=event \
    MYSQL_ROOT_PASSWORD=root 

ADD event.sql /docker-entrypoint-initdb.d

EXPOSE 3306