"""
MySQL database backup implementation.
"""
import os
from typing import Dict, Any, List
from .base import BaseDatabase, DatabaseBackupError


class MySQLDatabase(BaseDatabase):
    """MySQL database backup implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
    
    def get_backup_command(self) -> List[str]:
        """Get the mysqldump command."""
        command = ['mysqldump']
        
        # Add connection parameters
        if self.config.get('host'):
            command.extend(['-h', self.config['host']])
        
        if self.config.get('port'):
            command.extend(['-P', str(self.config['port'])])
        
        if self.config.get('user'):
            command.extend(['-u', self.config['user']])
        
        if self.config.get('password'):
            command.append(f"-p{self.config['password']}")
        
        # Add additional options
        command.extend(['--single-transaction', '--routines', '--triggers'])
        
        # Add database name
        if self.config.get('database'):
            command.append(self.config['database'])
        
        return command
    
    def backup(self) -> str:
        """
        Perform MySQL database backup.
        
        Returns:
            str: Path to the backup file
            
        Raises:
            DatabaseBackupError: If backup fails
        """
        backup_filename = self._generate_backup_filename('sql')
        backup_filepath = os.path.join(self.backup_dir, backup_filename)
        
        self.logger.info(f"Starting MySQL backup to {backup_filepath}")
        
        # Get backup command
        command = self.get_backup_command()
        
        # Run backup command
        success = self._run_command(command, backup_filepath)
        
        if not success:
            raise DatabaseBackupError("MySQL backup failed")
        
        # Verify backup file was created and has content
        if not os.path.exists(backup_filepath):
            raise DatabaseBackupError("Backup file was not created")
        
        if os.path.getsize(backup_filepath) == 0:
            raise DatabaseBackupError("Backup file is empty")
        
        self.logger.info(f"MySQL backup completed successfully: {backup_filepath}")
        return backup_filepath
