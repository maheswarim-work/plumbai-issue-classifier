.PHONY: help install test run clean docker-build docker-run docker-stop

# Default target
help:
	@echo "🚰 Smart Plumbing Issue Classifier API"
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  test         - Run tests"
	@echo "  run          - Start the API server"
	@echo "  clean        - Clean up generated files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"
	@echo "  docker-stop  - Stop Docker containers"
	@echo "  example      - Run example test script"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

# Run tests with coverage
test-cov:
	@echo "🧪 Running tests with coverage..."
	pytest tests/ --cov=app --cov-report=html --cov-report=term

# Start the API server
run:
	@echo "🚀 Starting Smart Plumbing Issue Classifier API..."
	python run.py

# Clean up generated files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f plumbing_classifier_model.pkl

# Build Docker image
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t plumbing-classifier .

# Run with Docker Compose
docker-run:
	@echo "🐳 Starting with Docker Compose..."
	docker-compose up -d

# Stop Docker containers
docker-stop:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

# Run example test script
example:
	@echo "🔧 Running example test script..."
	python examples/test_api.py

# Development setup
dev-setup: install
	@echo "🔧 Setting up development environment..."
	@echo "✅ Development environment ready!"
	@echo "   Run 'make run' to start the API"
	@echo "   Run 'make test' to run tests"
	@echo "   Run 'make example' to test the API"

# Production setup
prod-setup: docker-build
	@echo "🚀 Production environment ready!"
	@echo "   Run 'make docker-run' to start the API"
	@echo "   Run 'make docker-stop' to stop the API"

# Show API info
info:
	@echo "🚰 Smart Plumbing Issue Classifier API"
	@echo "📍 API: http://localhost:8000"
	@echo "📚 Docs: http://localhost:8000/docs"
	@echo "🔍 Health: http://localhost:8000/health" 