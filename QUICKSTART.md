# ⚡ Knowledge Assistant - Quick Start (5 min)

## What You'll Have
- AI assistant that answers questions about company knowledge
- Local LLM (no API calls, no costs)
- Web chat interface
- Export answers to Word/Excel
- Metrics & performance tracking

## Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama (https://ollama.ai)

## 1️⃣ Start Ollama
```bash
# Terminal 1: Start Ollama server
ollama serve

# Terminal 2: Download a model (first time only)
ollama pull qwen2.5:1.5b
```

## 2️⃣ Setup & Run
```bash
# Terminal 3: From project root
make setup    # One-time setup (installs dependencies, generates sample docs)
make run      # Starts backend + frontend
```

## 3️⃣ Open Browser
- **Chat**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 4️⃣ Try It Out
In the chat, ask:
- "How many vacation days do I get?"
- "What's the remote work policy?"
- "How do I set up the development environment?"

## Common Commands
```bash
# Add new documents
python backend/tools/synth_data.py  # Generate samples
# OR upload via UI

# Rebuild vector index
make reindex

# View metrics
make metrics

# Run evaluation
make eval

# Docker deployment
docker-compose up
```

## 📁 Where Things Happen
| Part | Location | What it does |
|------|----------|-------------|
| Chat UI | frontend/ | Browse, ask questions, export |
| Backend API | backend/main.py | Handles queries, reindexing |
| Documents | backend/data/raw/ | Add .md, .pdf, .docx files |
| Vector Store | backend/data/chroma_db/ | Auto-created, stores embeddings |
| LLM | Ollama (localhost:11434) | Generates answers |

## 🆘 Troubleshooting

**"Cannot connect to Ollama"**
- Ensure `ollama serve` is running
- Check port 11434 is open

**"Module not found"**
- Run: `cd backend && pip install -r requirements.txt`

**"Port already in use"**
- Change port in `.env` (backend) or package.json (frontend)

**No answers from AI**
- Make sure documents are indexed: `make reindex`
- Check backend logs: `tail -f /tmp/backend.log`

## 🎯 Next Steps
1. Add your own documents to `backend/data/raw/`
2. Run `make reindex`
3. Ask questions about your docs
4. Export answers to Word/Excel

---

👉 For full documentation, see **README.md**
