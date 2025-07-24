"""
Telegram notification implementation.
"""
import os
import requests
from typing import Dict, Any, Optional
from .base import BaseNotifier, NotificationError


class TelegramNotifier(BaseNotifier):
    """Telegram notification implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        if self.enabled:
            self._validate_config(['bot_token', 'chat_id'])
            self.bot_token = config['bot_token']
            self.chat_id = config['chat_id']
            self.api_base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_backup_success(self, backup_file: str, message: Optional[str] = None) -> bool:
        """
        Send backup success notification via Telegram.
        
        Args:
            backup_file: Path to the backup file
            message: Optional custom message
            
        Returns:
            bool: True if notification sent successfully
        """
        if not self.enabled:
            self.logger.debug("Telegram notifications are disabled")
            return True
        
        try:
            # First send a text message
            default_message = f"✅ Database backup completed successfully!\n\nBackup file: {os.path.basename(backup_file)}"
            text_message = message or default_message
            
            self._send_message(text_message)
            
            # Then send the backup file if it exists and is not too large
            if os.path.exists(backup_file) and os.path.getsize(backup_file) < 50 * 1024 * 1024:  # 50MB limit
                self._send_document(backup_file)
            else:
                self.logger.warning(f"Backup file {backup_file} is too large or doesn't exist, skipping file upload")
            
            self.logger.info("Telegram notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Telegram notification: {e}")
            return False
    
    def send_backup_failure(self, error_message: str) -> bool:
        """
        Send backup failure notification via Telegram.
        
        Args:
            error_message: Error message to send
            
        Returns:
            bool: True if notification sent successfully
        """
        if not self.enabled:
            self.logger.debug("Telegram notifications are disabled")
            return True
        
        try:
            message = f"❌ Database backup failed!\n\nError: {error_message}"
            self._send_message(message)
            
            self.logger.info("Telegram failure notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send Telegram failure notification: {e}")
            return False
    
    def _send_message(self, text: str) -> None:
        """
        Send a text message via Telegram API.
        
        Args:
            text: Message text to send
            
        Raises:
            NotificationError: If message sending fails
        """
        url = f"{self.api_base_url}/sendMessage"
        
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if not result.get('ok'):
            raise NotificationError(f"Telegram API error: {result.get('description', 'Unknown error')}")
    
    def _send_document(self, file_path: str) -> None:
        """
        Send a document via Telegram API.
        
        Args:
            file_path: Path to the file to send
            
        Raises:
            NotificationError: If document sending fails
        """
        url = f"{self.api_base_url}/sendDocument"
        
        data = {
            'chat_id': self.chat_id,
            'caption': f"Backup file: {os.path.basename(file_path)}"
        }
        
        with open(file_path, 'rb') as file:
            files = {'document': file}
            response = requests.post(url, data=data, files=files, timeout=120)
        
        response.raise_for_status()
        
        result = response.json()
        if not result.get('ok'):
            raise NotificationError(f"Telegram API error: {result.get('description', 'Unknown error')}")
