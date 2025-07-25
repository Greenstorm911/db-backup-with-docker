FROM python:3.11-alpine

# Install system dependencies
RUN apk add --no-cache \
    postgresql-client \
    mysql-client \
    zip \
    tzdata \
    && ln -sf /usr/share/zoneinfo/UTC /etc/localtime

# Create necessary directories
RUN mkdir -p /var/log/backup /backups /app

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY config/ ./config/
COPY src/ ./src/

# Set permissions
RUN chmod +x main.py && \
    touch /var/log/backup/backup.log

# Set Python path
ENV PYTHONPATH=/app

# Start cron in foreground and redirect cron output to stdout for Docker logs
CMD ["sh", "-c", "echo \"${CRON_SCHEDULE:-0 3 * * *} cd /app && python main.py\" > /etc/crontabs/root && chmod 0644 /etc/crontabs/root && busybox crond -f -L /dev/stdout"]