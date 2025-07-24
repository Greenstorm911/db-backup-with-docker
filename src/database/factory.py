"""
Database factory for creating database backup instances.
"""
from typing import Dict, Any
from .base import BaseDatabase
from .postgresql import PostgreSQLDatabase
from .mysql import MySQLDatabase


class DatabaseFactory:
    """Factory class for creating database backup instances."""
    
    _database_classes = {
        'postgresql': PostgreSQLDatabase,
        'postgres': PostgreSQLDatabase,  # Alias
        'mysql': MySQLDatabase,
        'mariadb': MySQLDatabase,  # Alias
    }
    
    @classmethod
    def create_database(cls, db_type: str, config: Dict[str, Any]) -> BaseDatabase:
        """
        Create a database backup instance based on the database type.
        
        Args:
            db_type: Type of database (postgresql, mysql, etc.)
            config: Database configuration
            
        Returns:
            BaseDatabase: Database backup instance
            
        Raises:
            ValueError: If database type is not supported
        """
        db_type_lower = db_type.lower()
        
        if db_type_lower not in cls._database_classes:
            supported_types = ', '.join(cls._database_classes.keys())
            raise ValueError(f"Unsupported database type: {db_type}. Supported types: {supported_types}")
        
        database_class = cls._database_classes[db_type_lower]
        return database_class(config)
    
    @classmethod
    def get_supported_types(cls) -> list:
        """Get list of supported database types."""
        return list(cls._database_classes.keys())
