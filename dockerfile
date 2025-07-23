FROM alpine:3.19

RUN apk add --no-cache postgresql-client curl zip tzdata
RUN ln -sf /usr/share/zoneinfo/UTC /etc/localtime
RUN mkdir -p /var/log/cron /backups

WORKDIR /app
COPY backup.sh .
COPY crontab /etc/crontabs/root

RUN chmod +x backup.sh && \
    chmod 0644 /etc/crontabs/root && \
    touch /var/log/cron/cron.log

CMD ["busybox", "crond", "-f", "-L", "/var/log/cron/cron.log"]