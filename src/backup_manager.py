"""
Main backup manager that orchestrates the backup process.
"""
import time
import logging
from typing import List, Optional
from config.config import config
from src.database import DatabaseFactory, DatabaseBackupError
from src.notification import NotificationFactory, BaseNotifier
from src.utils import compress_file, format_duration, get_file_size_mb


class BackupManager:
    """Main backup manager class."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.notifiers: List[BaseNotifier] = []
        
        # Initialize notifiers
        self._initialize_notifiers()
    
    def _initialize_notifiers(self) -> None:
        """Initialize notification providers."""
        try:
            # Create notifier configurations
            notifier_configs = {}
            
            if self.config.is_notification_enabled('telegram'):
                notifier_configs['telegram'] = self.config.get_notification_config('telegram')
            
            if self.config.is_notification_enabled('email'):
                notifier_configs['email'] = self.config.get_notification_config('email')
            
            # Create notifiers
            self.notifiers = NotificationFactory.create_all_notifiers(notifier_configs)
            
            if self.notifiers:
                self.logger.info(f"Initialized {len(self.notifiers)} notification providers")
            else:
                self.logger.info("No notification providers enabled")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize notifiers: {e}")
    
    def run_backup(self) -> bool:
        """
        Run the complete backup process.
        
        Returns:
            bool: True if backup completed successfully
        """
        start_time = time.time()
        backup_file = None
        
        try:
            self.logger.info("Starting database backup process")
            
            # Get database configuration
            db_config = self.config.get_database_config()
            db_type = db_config['type']
            
            self.logger.info(f"Database type: {db_type}")
            
            # Create database backup instance
            database = DatabaseFactory.create_database(db_type, db_config)
            
            # Perform backup
            backup_file = database.backup()
            backup_size_mb = get_file_size_mb(backup_file)
            
            self.logger.info(f"Backup created: {backup_file} ({backup_size_mb:.1f} MB)")
            
            # Compress backup if configured
            compressed_file = self._compress_backup(backup_file)
            if compressed_file:
                final_backup_file = compressed_file
                final_size_mb = get_file_size_mb(compressed_file)
                self.logger.info(f"Backup compressed: {compressed_file} ({final_size_mb:.1f} MB)")
            else:
                final_backup_file = backup_file
                final_size_mb = backup_size_mb
            
            # Clean up old backups
            backup_config = self.config.get_backup_config()
            retention_count = backup_config.get('retention_count', 3)
            database.cleanup_old_backups(retention_count)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Send success notifications
            success_message = self._create_success_message(
                final_backup_file, final_size_mb, duration
            )
            self._send_notifications('success', final_backup_file, success_message)
            
            self.logger.info(f"Backup process completed successfully in {format_duration(duration)}")
            return True
            
        except DatabaseBackupError as e:
            error_msg = f"Database backup failed: {e}"
            self.logger.error(error_msg)
            self._send_notifications('failure', None, error_msg)
            return False
            
        except Exception as e:
            error_msg = f"Unexpected error during backup: {e}"
            self.logger.error(error_msg, exc_info=True)
            self._send_notifications('failure', None, error_msg)
            return False
    
    def _compress_backup(self, backup_file: str) -> Optional[str]:
        """
        Compress the backup file if compression is enabled.
        
        Args:
            backup_file: Path to the backup file
            
        Returns:
            Optional[str]: Path to compressed file, or None if compression disabled/failed
        """
        backup_config = self.config.get_backup_config()
        compression_type = backup_config.get('compression')
        
        if not compression_type or compression_type.lower() == 'none':
            return None
        
        return compress_file(backup_file, compression_type)
    
    def _create_success_message(self, backup_file: str, size_mb: float, duration: float) -> str:
        """
        Create a success message for notifications.
        
        Args:
            backup_file: Path to the backup file
            size_mb: File size in MB
            duration: Backup duration in seconds
            
        Returns:
            str: Success message
        """
        import os
        from datetime import datetime
        
        db_config = self.config.get_database_config()
        
        message = f"""✅ Database backup completed successfully!

Database Details:
- Type: {db_config['type']}
- Host: {db_config['host']}
- Database: {db_config['database']}

Backup Details:
- File: {os.path.basename(backup_file)}
- Size: {size_mb:.1f} MB
- Duration: {format_duration(duration)}
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        return message
    
    def _send_notifications(self, notification_type: str, backup_file: Optional[str], message: str) -> None:
        """
        Send notifications to all configured providers.
        
        Args:
            notification_type: 'success' or 'failure'
            backup_file: Path to backup file (for success notifications)
            message: Message to send
        """
        if not self.notifiers:
            return
        
        for notifier in self.notifiers:
            try:
                if notification_type == 'success' and backup_file:
                    notifier.send_backup_success(backup_file, message)
                elif notification_type == 'failure':
                    notifier.send_backup_failure(message)
                    
            except Exception as e:
                self.logger.error(f"Failed to send notification via {notifier.__class__.__name__}: {e}")
