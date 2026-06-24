@'
# AI Knowledge Assistant - Makefile
# Usage: make <command>

# ── Setup ──────────────────────────────────────────
install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

# ── Data ───────────────────────────────────────────
synth:
	cd backend && python tools/synth_data.py

reindex:
	cd backend && python tools/build_index.py

# ── Run ────────────────────────────────────────────
run-ollama:
	ollama serve

run-backend:
	cd backend && uvicorn api.main:app --reload --port 8000

run-frontend:
	cd frontend && npm run dev

# ── Evaluate ───────────────────────────────────────
eval:
	cd backend && python tools/evaluate.py

logs:
	cd backend && python tools/analyze_logs.py

# ── Test ───────────────────────────────────────────
test-search:
	cd backend && python tools/test_search.py

test-api:
	curl -X POST http://localhost:8000/ask \
		-H "Authorization: Bearer secret-knowledge-token-2024" \
		-H "Content-Type: application/json" \
		-d "{\"question\": \"What is the leave policy?\"}"

# ── Clean ──────────────────────────────────────────
clean-index:
	rmdir /s /q backend\data\chroma_db

clean-logs:
	del /q backend\logs\*.jsonl
	del /q backend\logs\*.json

clean-all: clean-index clean-logs
	echo Cleaned index and logs.
'@ | Out-File -FilePath "Makefile" -Encoding utf8