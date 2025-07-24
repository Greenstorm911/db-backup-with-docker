"""
PostgreSQL database backup implementation.
"""
import os
from typing import Dict, Any, List
from .base import BaseDatabase, DatabaseBackupError


class PostgreSQLDatabase(BaseDatabase):
    """PostgreSQL database backup implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        # Set PostgreSQL password environment variable
        if config.get('password'):
            os.environ['PGPASSWORD'] = config['password']
    
    def get_backup_command(self) -> List[str]:
        """Get the pg_dump command."""
        command = ['pg_dump']
        
        # Add connection parameters
        if self.config.get('host'):
            command.extend(['-h', self.config['host']])
        
        if self.config.get('port'):
            command.extend(['-p', str(self.config['port'])])
        
        if self.config.get('user'):
            command.extend(['-U', self.config['user']])
        
        if self.config.get('database'):
            command.extend(['-d', self.config['database']])
        
        # Add additional options
        command.append('-w')  # Never prompt for password
        command.append('--verbose')  # Verbose output
        
        return command
    
    def backup(self) -> str:
        """
        Perform PostgreSQL database backup.
        
        Returns:
            str: Path to the backup file
            
        Raises:
            DatabaseBackupError: If backup fails
        """
        backup_filename = self._generate_backup_filename('sql')
        backup_filepath = os.path.join(self.backup_dir, backup_filename)
        
        self.logger.info(f"Starting PostgreSQL backup to {backup_filepath}")
        
        # Get backup command
        command = self.get_backup_command()
        
        # Run backup command
        success = self._run_command(command, backup_filepath)
        
        if not success:
            raise DatabaseBackupError("PostgreSQL backup failed")
        
        # Verify backup file was created and has content
        if not os.path.exists(backup_filepath):
            raise DatabaseBackupError("Backup file was not created")
        
        if os.path.getsize(backup_filepath) == 0:
            raise DatabaseBackupError("Backup file is empty")
        
        self.logger.info(f"PostgreSQL backup completed successfully: {backup_filepath}")
        return backup_filepath
