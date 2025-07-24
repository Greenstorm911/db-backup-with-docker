"""
Utility functions for the backup system.
"""
import os
import zipfile
import logging
from typing import Optional


def compress_file(source_file: str, compression_type: str = 'zip') -> Optional[str]:
    """
    Compress a file using the specified compression type.
    
    Args:
        source_file: Path to the source file
        compression_type: Type of compression ('zip', 'gzip', etc.)
        
    Returns:
        Optional[str]: Path to the compressed file, or None if compression failed
    """
    logger = logging.getLogger(__name__)
    
    if not os.path.exists(source_file):
        logger.error(f"Source file does not exist: {source_file}")
        return None
    
    try:
        if compression_type.lower() == 'zip':
            return _create_zip_file(source_file)
        else:
            logger.error(f"Unsupported compression type: {compression_type}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to compress file {source_file}: {e}")
        return None


def _create_zip_file(source_file: str) -> str:
    """
    Create a ZIP file from the source file.
    
    Args:
        source_file: Path to the source file
        
    Returns:
        str: Path to the created ZIP file
    """
    # Create ZIP filename
    base_name = os.path.splitext(source_file)[0]
    zip_file = f"{base_name}.zip"
    
    # Create ZIP file
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(source_file, os.path.basename(source_file))
    
    return zip_file


def setup_logging(log_level: str = 'INFO', log_file: Optional[str] = None) -> None:
    """
    Set up logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
    """
    # Create log directory if log file is specified
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Clear any existing handlers to avoid duplicates
    logging.getLogger().handlers.clear()
    
    handlers = []
    
    # Always add console handler for Docker logs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    handlers.append(console_handler)
    
    # Add file handler if log file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers,
        force=True  # Force reconfiguration
    )


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        str: Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        float: File size in MB
    """
    if not os.path.exists(file_path):
        return 0.0
    
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)
