FROM postgres:17-alpine
COPY service/schema.sql /docker-entrypoint-initdb.d/01-callpath.sql
