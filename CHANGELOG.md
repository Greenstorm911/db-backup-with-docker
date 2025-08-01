# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v1.1.0] - 2025-08-01

### Added
- **Multi-language support**: English and Persian (Farsi) for all messages, notifications, and logs
- **Complete Persian translation**: Full localization including README.fa.md
- **Language configuration**: LANGUAGE environment variable (en/fa)
- **Static project star promotion message** with disable option (SHOW_STAR_MESSAGE)
- **Translation framework**: Comprehensive `src/lang/translator.py` system
- **Persian README**: Complete documentation in Persian (README.fa.md)

### Changed
- Star promotion message is now static (not customizable) but includes disable instructions
- All system messages, notifications, and logs are now translatable
- Backup manager now uses translation system for all user-facing messages
- Configuration system enhanced to support language selection

### Enhanced
- Notification messages now display in selected language
- Error messages and logging output respect language setting
- Success notifications include localized formatting and content

## [v1.0.0] - 2025-08-01

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
- Docker Hub integration for easy image distribution
- Error handling and notification for backup failures

### Changed
- Migrated from shell script to Python for better maintainability
- Modular architecture with factory patterns for extensibility
- Enhanced error handling and logging capabilities

### Security
- Added vulnerability scanning with Trivy in CI pipeline
- Environment-based configuration to avoid hardcoded secrets
- Comprehensive documentation
