# Database Backup with Docker

[![Build and Push Docker Image](https://github.com/Greenstorm911/db-backup-with-docker/actions/workflows/docker-build-push.yml/badge.svg)](https://github.com/Greenstorm911/db-backup-with-docker/actions/workflows/docker-build-push.yml)
[![Test and Security Scan](https://github.com/Greenstorm911/db-backup-with-docker/actions/workflows/test.yml/badge.svg)](https://github.com/Greenstorm911/db-backup-with-docker/actions/workflows/test.yml)

A scalable, modular Python-based database backup system that supports multiple database types and notification providers. This system can be easily integrated into any Docker Compose setup to provide automated database backups.

## Features

- **Multiple Database Support**: PostgreSQL, MySQL/MariaDB with easy extensibility
- **Multiple Notification Providers**: Telegram, Email with modular architecture
- **Configurable Scheduling**: Customizable cron schedules
- **File Compression**: Optional ZIP compression for backup files
- **Backup Retention**: Automatic cleanup of old backup files
- **Error Handling**: Comprehensive error handling with detailed logging
- **Environment-based Configuration**: All settings via environment variables
- **Docker Ready**: Optimized for containerized deployments

## Project Structure

```
db-backup-with-docker/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── dockerfile             # Docker configuration
├── crontab                # Cron schedule configuration
├── config/
│   └── config.py          # Configuration management
└── src/
    ├── backup_manager.py  # Main backup orchestrator
    ├── database/          # Database backup modules
    │   ├── __init__.py
    │   ├── base.py        # Abstract base class
    │   ├── postgresql.py  # PostgreSQL implementation
    │   ├── mysql.py       # MySQL/MariaDB implementation
    │   └── factory.py     # Database factory
    ├── notification/      # Notification modules
    │   ├── __init__.py
    │   ├── base.py        # Abstract base class
    │   ├── telegram.py    # Telegram implementation
    │   ├── email.py       # Email implementation
    │   └── factory.py     # Notification factory
    └── utils/             # Utility functions
        ├── __init__.py
        └── helpers.py     # Helper functions
```

## Quick Start

### Option 1: Using Pre-built Image (Recommended)

Use the pre-built image from GitHub Container Registry:

```yaml
services:
  db-backup:
    container_name: backup
    image: ghcr.io/greenstorm911/db-backup-with-docker:latest
    depends_on:
      - db
    env_file: .env
    volumes:
      - backups:/backups
      - ./logs:/var/log/backup
    networks:
      - your-network
```

### Option 2: Building from Source

Clone this repository and build locally:

```yaml
services:
  db-backup:
    container_name: backup
    build:
      context: ./db-backup-with-docker
    depends_on:
      - db
    env_file: .env
    volumes:
      - backups:/backups
      - ./logs:/var/log/backup
    networks:
      - your-network

volumes:
  backups:
```

### 2. Environment Configuration

Create a `.env` file with the following variables:

#### Required Database Configuration
```env
# Database connection (REQUIRED)
DB_TYPE=postgresql              # or mysql, mariadb
DB_HOST=your-db-host
DB_PORT=5432                   # 5432 for PostgreSQL, 3306 for MySQL
DB_USER=your-username
DB_PASSWORD=your-password
DB_DATABASE=your-database-name
```

#### Optional Backup Configuration
```env
# Backup settings (OPTIONAL - defaults provided)
BACKUP_DIR=/backups
BACKUP_RETENTION_COUNT=3       # Number of backups to keep
BACKUP_COMPRESSION=zip         # zip or none
CRON_SCHEDULE=0 3 * * *       # Daily at 3 AM
```

#### Optional Telegram Notifications
```env
# Telegram notifications (OPTIONAL)
TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

#### Optional Email Notifications
```env
# Email notifications (OPTIONAL)
EMAIL_ENABLED=true
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
EMAIL_TO=recipient@example.com
```

#### Optional Logging Configuration
```env
# Logging (OPTIONAL - defaults provided)
LOG_LEVEL=INFO                 # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=/var/log/backup/backup.log
```

## Configuration Details

### Database Types

Currently supported database types:
- `postgresql` (or `postgres`)
- `mysql` 
- `mariadb` (uses MySQL client)

### Notification Providers

#### Telegram Setup
1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Get your chat ID (send a message to your bot, then visit: `https://api.telegram.org/bot<token>/getUpdates`)

#### Email Setup
For Gmail, use an app-specific password instead of your regular password.

### Backup Retention

The system automatically cleans up old backup files based on the `BACKUP_RETENTION_COUNT` setting. Both original SQL files and compressed ZIP files are managed.

## Usage Examples

### PostgreSQL with Telegram Notifications
```env
DB_TYPE=postgresql
DB_HOST=postgres
DB_PORT=5432
DB_USER=myuser
DB_PASSWORD=mypassword
DB_DATABASE=mydatabase

TELEGRAM_ENABLED=true
TELEGRAM_BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=123456789

BACKUP_RETENTION_COUNT=5
CRON_SCHEDULE=0 2 * * *
```

### MySQL with Email Notifications
```env
DB_TYPE=mysql
DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_PASSWORD=rootpassword
DB_DATABASE=app_database

EMAIL_ENABLED=true
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=backup@company.com
EMAIL_PASSWORD=app-specific-password
EMAIL_FROM=backup@company.com
EMAIL_TO=admin@company.com

BACKUP_COMPRESSION=zip
```

## Manual Backup

To run a backup manually:

```bash
docker exec backup python main.py
```

## Monitoring

### Logs

The system provides dual logging for maximum visibility:

- **Docker logs**: `docker logs backup` - Shows real-time output from the container
- **Log file**: `/var/log/backup/backup.log` - Persistent logs stored in mounted volume

#### Log Configuration
```env
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=/var/log/backup/backup.log    # Optional: file logging path
```

**Note**: Logs always appear in `docker logs` regardless of file logging configuration. This ensures you can monitor the backup process using standard Docker commands.

### Backup Files
Backup files are stored in the `backups` volume and follow this naming pattern:
- `backup_<database_name>_<timestamp>.sql`
- `backup_<database_name>_<timestamp>.zip` (if compression enabled)

## Troubleshooting

### Common Issues

1. **Missing Required Configuration**
   - Error: `Configuration error: Missing required configuration values`
   - Solution: Ensure all required database fields are set

2. **Database Connection Failed**
   - Check database host, port, credentials
   - Ensure database is accessible from the backup container

3. **Notification Failures**
   - Check notification provider credentials
   - Verify network connectivity
   - Check logs for specific error messages

4. **Permission Issues**
   - Ensure backup directory is writable
   - Check log directory permissions

### Debug Mode

Enable debug logging:
```env
LOG_LEVEL=DEBUG
```

## Extending the System

### Adding New Database Types

1. Create a new file in `src/database/` (e.g., `mongodb.py`)
2. Implement the `BaseDatabase` abstract class
3. Add the new class to `DatabaseFactory` in `factory.py`

### Adding New Notification Providers

1. Create a new file in `src/notification/` (e.g., `slack.py`)
2. Implement the `BaseNotifier` abstract class
3. Add the new class to `NotificationFactory` in `factory.py`

## Security Considerations

- Use environment variables for sensitive data
- Consider using Docker secrets for production
- Regularly rotate database passwords and API tokens
- Limit network access to backup containers
- Use app-specific passwords for email providers

## Development and Releases

### GitHub Actions

This project includes automated CI/CD workflows:

- **Build and Push**: Automatically builds and pushes Docker images to GitHub Container Registry on every push to main
- **Testing**: Runs Python linting and basic configuration tests
- **Security**: Scans for vulnerabilities using Trivy
- **Releases**: Creates multi-architecture builds and GitHub releases when you push a tag

### Creating a Release

1. Tag your release:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. The GitHub Action will automatically:
   - Build multi-architecture Docker images (amd64, arm64)
   - Push to `ghcr.io/greenstorm911/db-backup-with-docker:v1.0.0`
   - Create a GitHub release with changelog

### Development

Use the included Makefile for common tasks:
```bash
make help     # Show available commands
make build    # Build Docker image locally
make env      # Create .env from template
make backup   # Run one-time backup
make test     # Run tests
make lint     # Check code style
```

## License

This project is open source and available under the [MIT License](LICENSE).