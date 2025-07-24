#!/usr/bin/env python3
"""
Test script to verify logging configuration works properly.
"""
import sys
import logging
from src.utils import setup_logging

def test_logging():
    """Test the logging configuration."""
    # Test with file logging
    setup_logging('INFO', '/tmp/test.log')
    
    logger = logging.getLogger(__name__)
    logger.info("This should appear in both console and file")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("Check that logs appear in console (for Docker logs)")
    print("and also in the file /tmp/test.log")

if __name__ == "__main__":
    test_logging()
