#!/usr/bin/env python3
import sys
import logging
from config.config import config, ConfigError
from src.utils import setup_logging
from src.backup_manager import BackupManager


def main():

    try:

        log_config = config.get('logging', {})
        log_level = log_config.get('level', 'INFO')
        log_file = log_config.get('file')
        
        setup_logging(log_level, log_file)
        
        logger = logging.getLogger(__name__)
        logger.info("Starting database backup system")
        

        backup_manager = BackupManager()
        success = backup_manager.run_backup()
        
        if success:
            logger.info("Backup process completed successfully")
            sys.exit(0)
        else:
            logger.error("Backup process failed")
            sys.exit(1)
            
    except ConfigError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("Backup process interrupted by user", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
