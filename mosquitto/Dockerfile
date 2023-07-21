FROM alpine:edge

RUN adduser -S mosquitto
RUN apk update && apk upgrade
RUN apk add --no-cache mosquitto mosquitto-clients su-exec

COPY mosquitto.conf /etc/mosquitto/mosquitto.conf

EXPOSE 1883 9001

ADD start.sh /usr/bin/

CMD ["/usr/sbin/mosquitto", "-c", "/etc/mosquitto/mosquitto.conf"]
