FROM mysql:latest

ENV MYSQL_DATABASE=reservations \
    MYSQL_ROOT_PASSWORD=root 

ADD reservation.sql /docker-entrypoint-initdb.d

EXPOSE 3306