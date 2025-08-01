# سیستم پشتیبان‌گیری پایگاه داده با Docker

یک سیستم پشتیبان‌گیری مدرن و مدولار با Python برای پایگاه‌های داده PostgreSQL و MySQL/MariaDB با پشتیبانی از اطلاع‌رسانی‌های چندگانه و کانتینری‌سازی Docker.

## ویژگی‌های کلیدی

### 🗄️ پشتیبانی از پایگاه‌های داده
- **PostgreSQL**: پشتیبان‌گیری کامل با pg_dump
- **MySQL/MariaDB**: پشتیبان‌گیری کامل با mysqldump
- معماری قابل توسعه برای اضافه کردن پایگاه‌های داده جدید

### 📱 ارائه‌دهندگان اطلاع‌رسانی
- **Telegram**: ارسال پیام و فایل پشتیبان
- **Email**: اطلاع‌رسانی SMTP با پیوست فایل
- سیستم قابل توسعه برای روش‌های اطلاع‌رسانی جدید

### 🐳 کانتینری‌سازی Docker
- تصویر Alpine Linux سبک
- پشتیبانی از چند معماری (amd64, arm64)
- CI/CD خودکار با GitHub Actions
- منتشر شده در Docker Hub

### 🌐 پشتیبانی چندزبانه
- **انگلیسی** (en) - پیش‌فرض
- **فارسی** (fa) - کامل
- تمام پیام‌ها و اطلاع‌رسانی‌ها

### ⚙️ پیکربندی قدرتمند
- مبتنی بر متغیرهای محیطی
- اعتبارسنجی تنظیمات خودکار
- تنظیمات پشتیبان‌گیری منعطف

### 📊 مدیریت فایل پیشرفته
- فشرده‌سازی خودکار (ZIP)
- نگهداری پشتیبان قابل تنظیم
- پاک‌سازی خودکار فایل‌های قدیمی

## نصب سریع

### استفاده از Docker Compose (توصیه می‌شود)

1. **فایل docker-compose.yml ایجاد کنید:**

```yaml
services:
  db-backup:
    image: greenstorm911/db-backup-with-docker:latest
    environment:
      # تنظیمات پایگاه داده
      DB_TYPE: postgresql
      DB_HOST: your-db-host
      DB_PORT: 5432
      DB_USER: your-db-user
      DB_PASSWORD: your-db-password
      DB_DATABASE: your-database-name
      
      # تنظیمات پشتیبان‌گیری
      BACKUP_DIR: /backups
      BACKUP_RETENTION_COUNT: 3
      BACKUP_COMPRESSION: zip
      
      # زبان (اختیاری)
      LANGUAGE: fa  # 'en' برای انگلیسی، 'fa' برای فارسی
      
      # اطلاع‌رسانی تلگرام (اختیاری)
      TELEGRAM_ENABLED: true
      TELEGRAM_BOT_TOKEN: your-bot-token
      TELEGRAM_CHAT_ID: your-chat-id
      
      # تنظیمات لاگ
      LOG_LEVEL: INFO
      
    volumes:
      - ./backups:/backups
      - ./logs:/var/log/backup
    
    # برای اجرای دوره‌ای (اختیاری)
    environment:
      CRON_SCHEDULE: "0 3 * * *"  # روزانه ساعت 3 صبح
```

2. **اجرا کنید:**

```bash
docker-compose up -d
```

### اجرای دستی

```bash
docker run --rm \\
  -e DB_TYPE=postgresql \\
  -e DB_HOST=your-host \\
  -e DB_USER=your-user \\
  -e DB_PASSWORD=your-password \\
  -e DB_DATABASE=your-database \\
  -e LANGUAGE=fa \\
  -v ./backups:/backups \\
  greenstorm911/db-backup-with-docker:latest
```

## پیکربندی کامل

### فایل .env نمونه

```env
# تنظیمات پایگاه داده (اجباری)
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_DATABASE=your_database

# تنظیمات پشتیبان‌گیری
BACKUP_DIR=/backups
BACKUP_RETENTION_COUNT=3
BACKUP_COMPRESSION=zip

# تنظیمات تلگرام (اختیاری)
TELEGRAM_ENABLED=false
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# تنظیمات ایمیل (اختیاری)
EMAIL_ENABLED=false
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@gmail.com

# تنظیمات زمان‌بندی
CRON_SCHEDULE=0 3 * * *

# تنظیمات لاگ
LOG_LEVEL=INFO
LOG_FILE=/var/log/backup/backup.log

# زبان (اختیاری)
LANGUAGE=fa

# تبلیغ پروژه (اختیاری)
SHOW_STAR_MESSAGE=true
```

## انواع پایگاه داده

### PostgreSQL
```env
DB_TYPE=postgresql
DB_PORT=5432
```

### MySQL/MariaDB
```env
DB_TYPE=mysql
DB_PORT=3306
```

## ارائه‌دهندگان اطلاع‌رسانی

### تلگرام

1. ربات تلگرام ایجاد کنید و توکن دریافت کنید
2. Chat ID خود را پیدا کنید
3. تنظیمات را اضافه کنید:

```env
TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### ایمیل

```env
EMAIL_ENABLED=true
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient@gmail.com
```

## تنظیمات زبان

سیستم از دو زبان پشتیبانی می‌کند:

### انگلیسی (پیش‌فرض)
```env
LANGUAGE=en
```

### فارسی
```env
LANGUAGE=fa
```

تمام پیام‌ها، اطلاع‌رسانی‌ها و لاگ‌ها بر اساس زبان انتخابی نمایش داده می‌شوند.

## نگهداری پشتیبان

سیستم به طور خودکار پشتیبان‌های قدیمی را بر اساس تنظیم `BACKUP_RETENTION_COUNT` پاک می‌کند. هم فایل‌های SQL اصلی و هم فایل‌های ZIP فشرده مدیریت می‌شوند.

## نمونه‌های استفاده

### PostgreSQL با تلگرام (فارسی)

```yaml
services:
  db-backup:
    image: greenstorm911/db-backup-with-docker:latest
    environment:
      DB_TYPE: postgresql
      DB_HOST: postgres-server
      DB_USER: postgres
      DB_PASSWORD: mypassword
      DB_DATABASE: myapp
      LANGUAGE: fa
      TELEGRAM_ENABLED: true
      TELEGRAM_BOT_TOKEN: "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
      TELEGRAM_CHAT_ID: "987654321"
      CRON_SCHEDULE: "0 2 * * *"  # 2 صبح هر روز
    volumes:
      - ./backups:/backups
```

### MySQL با ایمیل (انگلیسی)

```yaml
services:
  db-backup:
    image: greenstorm911/db-backup-with-docker:latest
    environment:
      DB_TYPE: mysql
      DB_HOST: mysql-server
      DB_USER: root
      DB_PASSWORD: rootpassword
      DB_DATABASE: production
      LANGUAGE: en
      EMAIL_ENABLED: true
      EMAIL_SMTP_SERVER: smtp.gmail.com
      EMAIL_USERNAME: backup@company.com
      EMAIL_PASSWORD: app_password
      EMAIL_FROM: backup@company.com
      EMAIL_TO: admin@company.com
    volumes:
      - ./mysql-backups:/backups
```

## توسعه

### ساخت محلی

```bash
git clone https://github.com/Greenstorm911/db-backup-with-docker.git
cd db-backup-with-docker
docker build -t db-backup .
```

### افزودن زبان جدید

1. فایل `src/lang/translator.py` را ویرایش کنید
2. ترجمه‌های جدید را اضافه کنید
3. کد زبان را به تابع `_load_translations` اضافه کنید

### افزودن پایگاه داده جدید

1. کلاس جدید در `src/database/` ایجاد کنید
2. `BaseDatabase` را گسترش دهید
3. آن را به `DatabaseFactory` اضافه کنید

### افزودن ارائه‌دهنده اطلاع‌رسانی جدید

1. کلاس جدید در `src/notification/` ایجاد کنید
2. `BaseNotifier` را گسترش دهید
3. آن را به `NotificationFactory` اضافه کنید

## رفع اشکال

### مشاهده لاگ‌ها

```bash
# مشاهده لاگ‌های کانتینر
docker logs db-backup

# مشاهده لاگ‌های داخلی
docker exec db-backup tail -f /var/log/backup/backup.log
```

### مشاکل رایج

1. **اتصال پایگاه داده**: بررسی کنید host و port قابل دسترسی باشند
2. **مجوزهای فایل**: مطمئن شوید دایرکتوری پشتیبان قابل نوشتن است
3. **تنظیمات تلگرام**: Bot token و chat ID را تأیید کنید

## مشارکت

مشارکت‌ها خوش‌آمد است! لطفاً:

1. پروژه را Fork کنید
2. Branch ویژگی ایجاد کنید
3. تغییرات را Commit کنید
4. Pull Request ارسال کنید

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## حمایت

اگه این پروژه براتون مفید بود:

⭐ [GitHub Repository](https://github.com/Greenstorm911/db-backup-with-docker)

---

**نوت**: برای مستندات انگلیسی، [README.md](README.md) را مشاهده کنید.
