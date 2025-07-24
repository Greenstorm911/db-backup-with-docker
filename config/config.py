import os
import logging
from typing import Dict, Any, Optional


class ConfigError(Exception):
    pass


class Config:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:

        config = {

            'database': {
                'type': os.getenv('DB_TYPE', 'postgresql'),
                'host': os.getenv('DB_HOST'),
                'port': int(os.getenv('DB_PORT', 5432)),
                'user': os.getenv('DB_USER'),
                'password': os.getenv('DB_PASSWORD'),
                'database': os.getenv('DB_DATABASE'),
            },
            

            'backup': {
                'backup_dir': os.getenv('BACKUP_DIR', '/backups'),
                'retention_count': int(os.getenv('BACKUP_RETENTION_COUNT', 3)),
                'compression': os.getenv('BACKUP_COMPRESSION', 'zip'),
            },
            

            'telegram': {
                'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
                'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
                'enabled': os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true',
            },
            
            'email': {
                'smtp_server': os.getenv('EMAIL_SMTP_SERVER'),
                'smtp_port': int(os.getenv('EMAIL_SMTP_PORT', 587)),
                'username': os.getenv('EMAIL_USERNAME'),
                'password': os.getenv('EMAIL_PASSWORD'),
                'from_email': os.getenv('EMAIL_FROM'),
                'to_email': os.getenv('EMAIL_TO'),
                'enabled': os.getenv('EMAIL_ENABLED', 'false').lower() == 'true',
            },
            

            'cron': {
                'schedule': os.getenv('CRON_SCHEDULE', '0 3 * * *'),  # Daily at 3 AM
            },
            

            'logging': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'file': os.getenv('LOG_FILE', '/var/log/backup/backup.log'),
            }
        }
        
        self._validate_required_config(config)
        return config
    
    def _validate_required_config(self, config: Dict[str, Any]) -> None:

        required_fields = [
            ('database.host', config['database']['host']),
            ('database.user', config['database']['user']),
            ('database.password', config['database']['password']),
            ('database.database', config['database']['database']),
        ]
        
        missing_fields = []
        for field_name, field_value in required_fields:
            if not field_value:
                missing_fields.append(field_name)
        

        if config['telegram']['enabled']:
            if not config['telegram']['bot_token']:
                missing_fields.append('telegram.bot_token')
            if not config['telegram']['chat_id']:
                missing_fields.append('telegram.chat_id')
        
        if config['email']['enabled']:
            email_required = [
                ('email.smtp_server', config['email']['smtp_server']),
                ('email.username', config['email']['username']),
                ('email.password', config['email']['password']),
                ('email.from_email', config['email']['from_email']),
                ('email.to_email', config['email']['to_email']),
            ]
            for field_name, field_value in email_required:
                if not field_value:
                    missing_fields.append(field_name)
        
        if missing_fields:
            error_msg = f"Missing required configuration values: {', '.join(missing_fields)}"
            self.logger.error(error_msg)
            raise ConfigError(error_msg)
    
    def get(self, key: str, default: Any = None) -> Any:

        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            raise ConfigError(f"Configuration key '{key}' not found")
    
    def get_database_config(self) -> Dict[str, Any]:
        return self._config['database']
    
    def get_backup_config(self) -> Dict[str, Any]:
        return self._config['backup']
    
    def get_notification_config(self, provider: str) -> Dict[str, Any]:
        return self._config.get(provider, {})
    
    def is_notification_enabled(self, provider: str) -> bool:
        return self._config.get(provider, {}).get('enabled', False)



config = Config()
