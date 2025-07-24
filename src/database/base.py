"""
Base database backup module.
"""
import os
import subprocess
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class DatabaseBackupError(Exception):
    """Custom exception for database backup errors."""
    pass


class BaseDatabase(ABC):
    """Abstract base class for database backup implementations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.backup_dir = config.get('backup_dir', '/backups')
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
    
    @abstractmethod
    def backup(self) -> str:
        """
        Perform database backup and return the backup file path.
        
        Returns:
            str: Path to the backup file
            
        Raises:
            DatabaseBackupError: If backup fails
        """
        pass
    
    @abstractmethod
    def get_backup_command(self) -> list:
        """
        Get the backup command as a list of arguments.
        
        Returns:
            list: Command arguments for subprocess
        """
        pass
    
    def _generate_backup_filename(self, extension: str = 'sql') -> str:
        """Generate backup filename with timestamp."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        db_name = self.config.get('database', 'backup')
        return f"backup_{db_name}_{timestamp}.{extension}"
    
    def _run_command(self, command: list, output_file: Optional[str] = None) -> bool:
        """
        Run a command and return success status.
        
        Args:
            command: Command to run as list of arguments
            output_file: Optional output file for command output
            
        Returns:
            bool: True if command succeeded, False otherwise
        """
        try:
            self.logger.info(f"Running command: {' '.join(command)}")
            
            if output_file:
                with open(output_file, 'w') as f:
                    result = subprocess.run(
                        command,
                        stdout=f,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=True
                    )
            else:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            self.logger.info("Command executed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed with exit code {e.returncode}")
            self.logger.error(f"Error output: {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error running command: {e}")
            return False
    
    def cleanup_old_backups(self, retention_count: int = 3) -> None:
        """
        Clean up old backup files, keeping only the most recent ones.
        
        Args:
            retention_count: Number of backup files to keep
        """
        try:
            # Get all backup files in the backup directory
            backup_files = []
            for filename in os.listdir(self.backup_dir):
                if filename.startswith('backup_') and (filename.endswith('.sql') or filename.endswith('.zip')):
                    filepath = os.path.join(self.backup_dir, filename)
                    backup_files.append((filepath, os.path.getmtime(filepath)))
            
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove old files
            files_to_remove = backup_files[retention_count:]
            for filepath, _ in files_to_remove:
                os.remove(filepath)
                self.logger.info(f"Removed old backup file: {filepath}")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up old backups: {e}")
