.PHONY: help build run test clean lint

# Default target
help:
	@echo "Available targets:"
	@echo "  build     - Build Docker image"
	@echo "  run       - Run container with example environment"
	@echo "  test      - Run tests and linting"
	@echo "  clean     - Clean up Docker images and containers"
	@echo "  lint      - Run code linting"
	@echo "  logs      - Show container logs"

# Build Docker image
build:
	docker build -t db-backup:latest -f dockerfile .

# Run container (you need to provide your own .env file)
run:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Copy .env.example to .env and configure it."; \
		exit 1; \
	fi
	docker run --rm --env-file .env -v $(PWD)/backups:/backups db-backup:latest

# Run one-time backup (manual trigger)
backup:
	@if [ ! -f .env ]; then \
		echo "Error: .env file not found. Copy .env.example to .env and configure it."; \
		exit 1; \
	fi
	docker run --rm --env-file .env -v $(PWD)/backups:/backups db-backup:latest python main.py

# Run tests
test:
	python -m pytest tests/ -v --cov=src/

# Lint code
lint:
	flake8 src/ config/ main.py
	python -m black --check src/ config/ main.py

# Format code
format:
	python -m black src/ config/ main.py

# Clean up Docker resources
clean:
	docker container prune -f
	docker image prune -f
	docker rmi db-backup:latest 2>/dev/null || true

# Show logs from running container
logs:
	docker logs -f db-backup 2>/dev/null || echo "No container named 'db-backup' is running"

# Create .env from example
env:
	@if [ -f .env ]; then \
		echo ".env file already exists"; \
	else \
		cp .env.example .env; \
		echo ".env file created from .env.example - please edit it with your configuration"; \
	fi
