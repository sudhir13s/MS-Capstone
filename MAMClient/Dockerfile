FROM alpine:edge
RUN apk update && apk upgrade

RUN apk update && apk upgrade && \
    apk add redis

EXPOSE 6379

CMD ["redis-server", "--protected-mode no"]