"""Translation system for multi-language support."""

import os
from typing import Dict, Any, Optional


class Translator:
    """Translation system supporting English and Persian."""
    
    def __init__(self, language: str = 'en'):
        """
        Initialize translator.
        
        Args:
            language: Language code ('en' for English, 'fa' for Persian)
        """
        self.language = language.lower()
        self.translations = self._load_translations()
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load all translations."""
        return {
            'en': {
                # Database backup messages
                'backup_starting': 'Starting database backup process',
                'backup_completed': 'Database backup completed successfully!',
                'backup_failed': 'Database backup failed',
                'backup_created': 'Backup created: {file} ({size:.1f} MB)',
                'backup_compressed': 'Backup compressed: {file} ({size:.1f} MB)',
                'backup_process_completed': 'Backup process completed successfully in {duration}',
                'unexpected_error': 'Unexpected error during backup: {error}',
                
                # Database details
                'database_details': 'Database Details',
                'database_type': 'Type',
                'database_host': 'Host',
                'database_name': 'Database',
                
                # Backup details
                'backup_details': 'Backup Details',
                'backup_file': 'File',
                'backup_size': 'Size',
                'backup_duration': 'Duration',
                'backup_timestamp': 'Timestamp',
                
                # Notification messages
                'notification_init_success': 'Initialized {count} notification providers',
                'notification_init_none': 'No notification providers enabled',
                'notification_init_failed': 'Failed to initialize notifiers: {error}',
                'notification_send_failed': 'Failed to send notification via {provider}: {error}',
                
                # Validation messages
                'config_missing_fields': 'Missing required configuration values: {fields}',
                'config_key_not_found': 'Configuration key \'{key}\' not found',
                
                # File operations
                'file_compression_failed': 'Failed to compress backup file: {error}',
                'file_cleanup_old_backups': 'Cleaning up old backups, keeping {count} most recent',
                'file_cleanup_completed': 'Cleanup completed: removed {count} old backup files',
                
                # Success/failure indicators
                'success_indicator': '✅',
                'failure_indicator': '❌',
                'warning_indicator': '⚠️',
                'info_indicator': 'ℹ️',
                
                # Promotion message
                'star_message': '⭐ If this backup tool is helpful, please consider starring the project on GitHub: https://github.com/Greenstorm911/db-backup-with-docker\\n💡 You can disable this message by setting SHOW_STAR_MESSAGE=false in your .env file ⭐',
                'star_message_disable_info': 'You can disable this message by setting SHOW_STAR_MESSAGE=false in your .env file',
                
                # Time and duration
                'duration_seconds': '{seconds:.1f} seconds',
                'duration_minutes': '{minutes:.1f} minutes',
                'duration_hours': '{hours:.1f} hours',
            },
            
            'fa': {
                # Database backup messages (Persian/Farsi)
                'backup_starting': 'شروع فرآیند پشتیبان‌گیری از پایگاه داده',
                'backup_completed': 'پشتیبان‌گیری از پایگاه داده با موفقیت تکمیل شد!',
                'backup_failed': 'پشتیبان‌گیری از پایگاه داده ناموفق بود',
                'backup_created': 'پشتیبان ایجاد شد: {file} ({size:.1f} مگابایت)',
                'backup_compressed': 'پشتیبان فشرده شد: {file} ({size:.1f} مگابایت)',
                'backup_process_completed': 'فرآیند پشتیبان‌گیری با موفقیت در {duration} تکمیل شد',
                'unexpected_error': 'خطای غیرمنتظره در حین پشتیبان‌گیری: {error}',
                
                # Database details
                'database_details': 'جزئیات پایگاه داده',
                'database_type': 'نوع',
                'database_host': 'میزبان',
                'database_name': 'پایگاه داده',
                
                # Backup details
                'backup_details': 'جزئیات پشتیبان',
                'backup_file': 'فایل',
                'backup_size': 'اندازه',
                'backup_duration': 'مدت زمان',
                'backup_timestamp': 'زمان',
                
                # Notification messages
                'notification_init_success': '{count} ارائه‌دهنده اطلاع‌رسانی راه‌اندازی شد',
                'notification_init_none': 'هیچ ارائه‌دهنده اطلاع‌رسانی فعال نیست',
                'notification_init_failed': 'راه‌اندازی اطلاع‌رسان‌ها ناموفق بود: {error}',
                'notification_send_failed': 'ارسال اطلاع‌رسانی از طریق {provider} ناموفق بود: {error}',
                
                # Validation messages
                'config_missing_fields': 'مقادیر تنظیمات مورد نیاز موجود نیست: {fields}',
                'config_key_not_found': 'کلید تنظیمات \'{key}\' یافت نشد',
                
                # File operations
                'file_compression_failed': 'فشرده‌سازی فایل پشتیبان ناموفق بود: {error}',
                'file_cleanup_old_backups': 'پاک‌سازی پشتیبان‌های قدیمی، نگهداری {count} مورد اخیر',
                'file_cleanup_completed': 'پاک‌سازی تکمیل شد: {count} فایل پشتیبان قدیمی حذف شد',
                
                # Success/failure indicators
                'success_indicator': '✅',
                'failure_indicator': '❌',
                'warning_indicator': '⚠️',
                'info_indicator': 'ℹ️',
                
                # Promotion message
                'star_message': '⭐ اگر این ابزار پشتیبان‌گیری مفید است، لطفاً پروژه را در GitHub ستاره دهید: https://github.com/Greenstorm911/db-backup-with-docker\\n💡 می‌توانید این پیام را با تنظیم SHOW_STAR_MESSAGE=false در فایل .env خود غیرفعال کنید ⭐',
                'star_message_disable_info': 'می‌توانید این پیام را با تنظیم SHOW_STAR_MESSAGE=false در فایل .env خود غیرفعال کنید',
                
                # Time and duration
                'duration_seconds': '{seconds:.1f} ثانیه',
                'duration_minutes': '{minutes:.1f} دقیقه',
                'duration_hours': '{hours:.1f} ساعت',
            }
        }
    
    def translate(self, key: str, **kwargs) -> str:
        """
        Translate a message key to the current language.
        
        Args:
            key: Translation key
            **kwargs: Format parameters for the message
            
        Returns:
            str: Translated message
        """
        translations = self.translations.get(self.language, self.translations['en'])
        message = translations.get(key, key)
        
        if kwargs:
            try:
                return message.format(**kwargs)
            except (KeyError, ValueError):
                return message
        
        return message
    
    def set_language(self, language: str) -> None:
        """Set the current language."""
        self.language = language.lower()
    
    def get_available_languages(self) -> list:
        """Get list of available language codes."""
        return list(self.translations.keys())


# Global translator instance
_translator = None

def get_translator() -> Translator:
    """Get the global translator instance."""
    global _translator
    if _translator is None:
        # Get language from environment, default to English
        language = os.getenv('LANGUAGE', 'en').lower()
        _translator = Translator(language)
    return _translator

def t(key: str, **kwargs) -> str:
    """
    Shorthand function for translation.
    
    Args:
        key: Translation key
        **kwargs: Format parameters
        
    Returns:
        str: Translated message
    """
    return get_translator().translate(key, **kwargs)
