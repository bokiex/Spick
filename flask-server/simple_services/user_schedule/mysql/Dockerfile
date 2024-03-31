FROM mysql:latest
ENV MYSQL_DATABASE=user_schedule \
    MYSQL_ROOT_PASSWORD=root

ADD user_schedule.sql /docker-entrypoint-initdb.d

EXPOSE 3306

