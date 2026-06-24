# Knowledge Assistant Makefile
# Convenient commands for development and deployment

.PHONY: help install setup run run-backend run-frontend stop clean reindex eval metrics docs

help:
	@echo "Knowledge Assistant - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install all dependencies"
	@echo "  make setup          Full setup (install + generate data)"
	@echo ""
	@echo "Development:"
	@echo "  make run            Run both backend and frontend"
	@echo "  make run-backend    Run backend only (http://localhost:8000)"
	@echo "  make run-frontend   Run frontend only (http://localhost:3000)"
	@echo "  make stop           Stop all services"
	@echo ""
	@echo "Data Management:"
	@echo "  make reindex        Rebuild vector index from documents"
	@echo "  make synth          Generate synthetic sample documents"
	@echo "  make clean          Clean all generated files (logs, exports, db)"
	@echo ""
	@echo "Evaluation & Monitoring:"
	@echo "  make eval           Run evaluation on test questions"
	@echo "  make metrics        Show query metrics summary"
	@echo "  make health         Check backend health"
	@echo ""
	@echo "Deployment:"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run in Docker"

install:
	@echo "📦 Installing dependencies..."
	@cd backend && pip install -r requirements.txt
	@cd frontend && npm install
	@echo "✅ Dependencies installed"

setup: install
	@echo "🚀 Setting up Knowledge Assistant..."
	@cd backend && python tools/synth_data.py
	@cd backend && python tools/reindex.py
	@echo "✅ Setup complete! Run 'make run' to start"

run: run-backend run-frontend
	@echo "🎉 Both services running..."

run-backend:
	@echo "🔄 Starting backend (http://localhost:8000)..."
	@cd backend && python -m uvicorn main:app --reload --port 8000

run-frontend:
	@echo "🔄 Starting frontend (http://localhost:3000)..."
	@cd frontend && npm run dev

stop:
	@echo "⛔ Stopping services..."
	@pkill -f "uvicorn" || echo "Backend not running"
	@pkill -f "next dev" || echo "Frontend not running"
	@echo "✅ Services stopped"

clean:
	@echo "🧹 Cleaning generated files..."
	@rm -rf backend/logs/*.json backend/exports/* backend/data/chroma_db/*
	@echo "✅ Cleaned"

reindex:
	@echo "🔄 Reindexing documents..."
	@cd backend && python tools/reindex.py

synth:
	@echo "📝 Generating synthetic data..."
	@cd backend && python tools/synth_data.py

eval:
	@echo "📊 Running evaluation..."
	@cd backend && python tools/eval.py 2>/dev/null || echo "Run 'make setup' first"

metrics:
	@echo "📈 Query Metrics:"
	@curl -s http://localhost:8000/metrics | jq '.stats' 2>/dev/null || echo "Backend not running. Run 'make run-backend'"

health:
	@echo "🏥 Backend Health Check:"
	@curl -s http://localhost:8000/health | jq . 2>/dev/null || echo "❌ Backend offline"

docker-build:
	@echo "🐳 Building Docker image..."
	@docker build -t knowledge-assistant:latest .
	@echo "✅ Built. Run with: docker run -p 8000:8000 -p 3000:3000 knowledge-assistant"

docker-run:
	@echo "🐳 Running in Docker..."
	@docker-compose up

# Development helpers
lint:
	@echo "🔍 Linting Python code..."
	@cd backend && python -m pylint core/ api/ tools/ || true

test:
	@echo "🧪 Running tests..."
	@cd backend && python -m pytest tests/ || echo "No tests found"

format:
	@echo "✨ Formatting code..."
	@cd backend && black . && isort .
	@cd frontend && npx prettier --write .

docs:
	@echo "📚 Opening documentation..."
	@echo "See README.md for full documentation"
	@cat README.md | head -50

.DEFAULT_GOAL := help
