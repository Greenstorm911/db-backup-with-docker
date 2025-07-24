"""
Notification factory for creating notification instances.
"""
from typing import Dict, Any, List
from .base import BaseNotifier
from .telegram import TelegramNotifier
from .email import EmailNotifier


class NotificationFactory:
    """Factory class for creating notification instances."""
    
    _notifier_classes = {
        'telegram': TelegramNotifier,
        'email': EmailNotifier,
    }
    
    @classmethod
    def create_notifier(cls, notifier_type: str, config: Dict[str, Any]) -> BaseNotifier:
        """
        Create a notification instance based on the notifier type.
        
        Args:
            notifier_type: Type of notifier (telegram, email, etc.)
            config: Notification configuration
            
        Returns:
            BaseNotifier: Notification instance
            
        Raises:
            ValueError: If notifier type is not supported
        """
        notifier_type_lower = notifier_type.lower()
        
        if notifier_type_lower not in cls._notifier_classes:
            supported_types = ', '.join(cls._notifier_classes.keys())
            raise ValueError(f"Unsupported notifier type: {notifier_type}. Supported types: {supported_types}")
        
        notifier_class = cls._notifier_classes[notifier_type_lower]
        return notifier_class(config)
    
    @classmethod
    def create_all_notifiers(cls, configs: Dict[str, Dict[str, Any]]) -> List[BaseNotifier]:
        """
        Create all notification instances from configurations.
        
        Args:
            configs: Dictionary of notification configurations
            
        Returns:
            List[BaseNotifier]: List of notification instances
        """
        notifiers = []
        
        for notifier_type, config in configs.items():
            if notifier_type in cls._notifier_classes and config.get('enabled', False):
                try:
                    notifier = cls.create_notifier(notifier_type, config)
                    notifiers.append(notifier)
                except Exception as e:
                    # Log error but continue with other notifiers
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Failed to create {notifier_type} notifier: {e}")
        
        return notifiers
    
    @classmethod
    def get_supported_types(cls) -> List[str]:
        """Get list of supported notifier types."""
        return list(cls._notifier_classes.keys())
