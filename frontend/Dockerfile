FROM node:alpine

ARG USER

COPY docker-entrypoint.sh /docker-entrypoint.sh

WORKDIR /app

RUN chmod +x /docker-entrypoint.sh \
    && adduser -D -s /bin/bash $USER \
    && chown $USER:$USER /app

#USER $USER

EXPOSE 8080