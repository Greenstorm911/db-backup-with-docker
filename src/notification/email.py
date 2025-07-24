"""
Email notification implementation.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, Optional
from .base import BaseNotifier, NotificationError


class EmailNotifier(BaseNotifier):
    """Email notification implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        if self.enabled:
            self._validate_config(['smtp_server', 'username', 'password', 'from_email', 'to_email'])
            self.smtp_server = config['smtp_server']
            self.smtp_port = config.get('smtp_port', 587)
            self.username = config['username']
            self.password = config['password']
            self.from_email = config['from_email']
            self.to_email = config['to_email']
    
    def send_backup_success(self, backup_file: str, message: Optional[str] = None) -> bool:
        """
        Send backup success notification via email.
        
        Args:
            backup_file: Path to the backup file
            message: Optional custom message
            
        Returns:
            bool: True if notification sent successfully
        """
        if not self.enabled:
            self.logger.debug("Email notifications are disabled")
            return True
        
        try:
            subject = "✅ Database Backup Completed Successfully"
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = subject
            
            # Email body
            default_body = f"""
Database backup completed successfully!

Backup Details:
- File: {os.path.basename(backup_file)}
- Size: {self._format_file_size(backup_file)}
- Path: {backup_file}
- Timestamp: {self._get_file_timestamp(backup_file)}

The backup file is attached to this email (if under size limit).
"""
            
            body = message or default_body
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach backup file if it exists and is not too large (10MB limit for email)
            if os.path.exists(backup_file) and os.path.getsize(backup_file) < 10 * 1024 * 1024:
                self._attach_file(msg, backup_file)
            else:
                msg.attach(MIMEText("\nNote: Backup file is too large to attach via email.", 'plain'))
            
            # Send email
            self._send_email(msg)
            
            self.logger.info("Email notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {e}")
            return False
    
    def send_backup_failure(self, error_message: str) -> bool:
        """
        Send backup failure notification via email.
        
        Args:
            error_message: Error message to send
            
        Returns:
            bool: True if notification sent successfully
        """
        if not self.enabled:
            self.logger.debug("Email notifications are disabled")
            return True
        
        try:
            subject = "❌ Database Backup Failed"
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = subject
            
            # Email body
            body = f"""
Database backup failed!

Error Details:
{error_message}

Please check the backup system and resolve the issue.
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            self._send_email(msg)
            
            self.logger.info("Email failure notification sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email failure notification: {e}")
            return False
    
    def _send_email(self, msg: MIMEMultipart) -> None:
        """
        Send email via SMTP.
        
        Args:
            msg: Email message to send
            
        Raises:
            NotificationError: If email sending fails
        """
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            text = msg.as_string()
            server.sendmail(self.from_email, self.to_email, text)
            server.quit()
            
        except Exception as e:
            raise NotificationError(f"Failed to send email: {e}")
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str) -> None:
        """
        Attach a file to the email message.
        
        Args:
            msg: Email message
            file_path: Path to the file to attach
        """
        with open(file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(file_path)}',
        )
        
        msg.attach(part)
    
    def _format_file_size(self, file_path: str) -> str:
        """Format file size in human-readable format."""
        if not os.path.exists(file_path):
            return "Unknown"
        
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def _get_file_timestamp(self, file_path: str) -> str:
        """Get file modification timestamp."""
        if not os.path.exists(file_path):
            return "Unknown"
        
        import datetime
        timestamp = os.path.getmtime(file_path)
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
