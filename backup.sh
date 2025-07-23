#!/bin/sh


. /etc/profile


echo "Cron environment:" >> /var/log/cron/cron.log
env >> /var/log/cron/cron.log


echo "Starting backup at $(date)" >> /var/log/cron/cron.log

export PGPASSWORD=$PG_PASSWORD

TELEGRAM_API="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_heymlz_shop${TIMESTAMP}.sql"
ZIP_FILE="backup_heymlz_shop${TIMESTAMP}.zip"


pg_dump -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DATABASE -w > /backups/$BACKUP_FILE

if [ $? -ne 0 ]; then
  echo "backup failed" >> /var/log/cron/cron.log
  exit 1
fi

zip -j /backups/$ZIP_FILE /backups/$BACKUP_FILE
curl -F chat_id=$TELEGRAM_CHAT_ID \
     -F document=@/backups/$ZIP_FILE \
     $TELEGRAM_API


ls -t /backups/*.zip | tail -n +4 | xargs rm -f
ls -t /backups/*.sql | tail -n +4 | xargs rm -f
echo "backup completed at $(date)" >> /var/log/cron/cron.log