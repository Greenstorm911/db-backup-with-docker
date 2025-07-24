# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of Python-based modular backup system
- Support for PostgreSQL and MySQL/MariaDB databases
- Telegram and Email notification providers
- Docker containerization with Alpine Linux base
- GitHub Actions CI/CD pipeline for automated builds
- Multi-architecture Docker image support (amd64, arm64)
- Comprehensive configuration management with environment variables
- Automatic backup cleanup with configurable retention policies
- File compression support (ZIP)
- Structured logging with dual output (console + file)
- Error handling and notification for backup failures

### Changed
- Migrated from shell script to Python for better maintainability
- Modular architecture with factory patterns for extensibility
- Enhanced error handling and logging capabilities

### Security
- Added vulnerability scanning with Trivy in CI pipeline
- Environment-based configuration to avoid hardcoded secrets

## [v1.0.0] - 2025-07-24

### Added
- Complete rewrite of backup system in Python
- Modular database support (PostgreSQL, MySQL/MariaDB)
- Multiple notification providers (Telegram, Email)
- Docker containerization
- GitHub Actions workflows
- Comprehensive documentation
