"""
Base notification module.
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class NotificationError(Exception):
    """Custom exception for notification errors."""
    pass


class BaseNotifier(ABC):
    """Abstract base class for notification implementations."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.enabled = config.get('enabled', False)
    
    @abstractmethod
    def send_backup_success(self, backup_file: str, message: Optional[str] = None) -> bool:
        """
        Send notification for successful backup.
        
        Args:
            backup_file: Path to the backup file
            message: Optional custom message
            
        Returns:
            bool: True if notification sent successfully
        """
        pass
    
    @abstractmethod
    def send_backup_failure(self, error_message: str) -> bool:
        """
        Send notification for backup failure.
        
        Args:
            error_message: Error message to send
            
        Returns:
            bool: True if notification sent successfully
        """
        pass
    
    def is_enabled(self) -> bool:
        """Check if this notifier is enabled."""
        return self.enabled
    
    def _validate_config(self, required_fields: list) -> None:
        """
        Validate that required configuration fields are present.
        
        Args:
            required_fields: List of required field names
            
        Raises:
            NotificationError: If required fields are missing
        """
        missing_fields = []
        for field in required_fields:
            if not self.config.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            raise NotificationError(f"Missing required configuration fields: {', '.join(missing_fields)}")
