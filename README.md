# Knowledge Assistant - Complete Project

A production-ready AI Knowledge Assistant that demonstrates a complete RAG (Retrieval-Augmented Generation) pipeline with local LLM support. Perfect for onboarding engineers or understanding how modern AI systems work.

## 🎯 Project Completion Status: ✅ 100%

All major components implemented:
- ✅ Synthetic data generation (9 comprehensive documents)
- ✅ Document ingestion & parsing (Markdown, PDF, DOCX, CSV, JSON, TXT)
- ✅ Text chunking with configurable overlap
- ✅ Embeddings & vector store (Chroma + Sentence-Transformers)
- ✅ RAG pipeline (retrieval + LLM generation)
- ✅ Answer generation with citations
- ✅ FastAPI backend with full endpoint coverage
- ✅ React/Next.js frontend with chat interface
- ✅ Export to Word & Excel
- ✅ Metrics tracking & evaluation logging
- ✅ Document upload & reindexing

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **Ollama** installed and running (for local LLM)
- **PostgreSQL** (optional, for production)

### 1. Install Ollama (Local LLM)

Download from [ollama.ai](https://ollama.ai)

```bash
# Start Ollama (runs on localhost:11434)
ollama serve

# In another terminal, pull a model
ollama pull qwen2.5:1.5b  # ~1.5B params, fast & lightweight
# OR
ollama pull mistral       # ~7B params, better quality
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env if using different Ollama model

# Generate synthetic documents
python tools/synth_data.py

# Build vector index (required before first use)
python tools/reindex.py

# Start backend server
uvicorn main:app --reload --port 8000
```

Backend runs at: **http://localhost:8000**  
API docs at: **http://localhost:8000/docs**

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Edit if backend is on different port

# Start dev server
npm run dev
```

Frontend runs at: **http://localhost:3000**

## 📚 Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Frontend (React/Next.js)                                │
│ - Chat interface with message history                   │
│ - Export to Word/Excel                                  │
│ - Document upload & reindex UI                          │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│ Backend API (FastAPI)                                   │
│ ├─ /ask          → RAG query pipeline                   │
│ ├─ /export/*     → Document export                      │
│ ├─ /upload       → File upload                          │
│ ├─ /reindex      → Rebuild vector store                 │
│ ├─ /metrics      → Query statistics                     │
│ └─ /health       → Status check                         │
└────────────────────┬────────────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     │               │               │
┌────▼────┐  ┌──────▼──────┐  ┌─────▼──────┐
│  Chroma  │  │   Sentence  │  │   Ollama   │
│ Vector   │  │ Transformers│  │    LLM     │
│ Database │  │ Embeddings  │  │            │
└──────────┘  └─────────────┘  └────────────┘
```

## 🔄 RAG Pipeline Flow

```
User Question
    ↓
Embed question (Sentence-Transformers)
    ↓
Search similar chunks in Chroma (semantic similarity)
    ↓
Retrieve top-5 relevant documents
    ↓
Build prompt with context + question
    ↓
Send to Ollama LLM for generation
    ↓
Format answer with citations
    ↓
Log metrics (latency, sources, citations)
    ↓
Return to user
```

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Configuration template
│   │
│   ├── api/
│   │   └── routes.py         # All API endpoints
│   │
│   ├── core/
│   │   ├── config.py         # Ollama & env config
│   │   ├── chunking.py       # Text splitting logic
│   │   ├── parser.py         # Multi-format document parsing
│   │   ├── ingestion.py      # Load & normalize documents
│   │   ├── vector_store.py   # Chroma wrapper
│   │   ├── rag.py            # RAG pipeline (query → answer)
│   │   ├── logger.py         # Metrics & telemetry
│   │   ├── llm.py            # LLM interface
│   │   └── exporter.py       # DOCX/XLSX export
│   │
│   ├── data/
│   │   ├── raw/              # Input documents (Markdown, PDF, etc.)
│   │   ├── chroma_db/        # Vector store (auto-created)
│   │   └── processed/        # Processed docs (if needed)
│   │
│   ├── tools/
│   │   ├── synth_data.py     # Generate sample documents
│   │   ├── reindex.py        # Rebuild vector index
│   │   └── eval.py           # Evaluation metrics (optional)
│   │
│   ├── logs/
│   │   ├── metrics.json      # Query logs & stats
│   │   └── queries.jsonl     # Individual query records
│   │
│   └── exports/
│       ├── answer.docx       # Generated Word files
│       └── answer.xlsx       # Generated Excel files
│
└── frontend/
    ├── package.json          # Node dependencies
    ├── next.config.ts        # Next.js config
    ├── .env.example          # Frontend env template
    ├── tsconfig.json         # TypeScript config
    │
    ├── app/
    │   ├── layout.tsx        # Root layout
    │   ├── page.js           # Main page (home)
    │   └── globals.css       # Global styles
    │
    ├── components/
    │   ├── ChatBox.js        # Chat interface
    │   ├── Message.js        # Message display
    │   ├── Sidebar.js        # Chat history
    │   └── LatencyChart.js   # Performance metrics
    │
    ├── lib/
    │   └── api.js            # API client
    │
    ├── utils/
    │   └── storage.js        # Local storage for chat history
    │
    └── public/               # Static assets
```

## 🎓 Key Concepts Demonstrated

### 1. **Semantic Search (Vector Embeddings)**
- Documents are encoded into high-dimensional vectors
- Search finds semantically similar content, not just keyword matches
- Example: "Leave policy" and "vacation days" will match

### 2. **Chunking Strategy**
- Documents split into overlapping chunks (default: 500 words, 100 overlap)
- Prevents context loss at chunk boundaries
- Configurable per use case

### 3. **RAG Pattern**
- Retrieve context → Generate answer → Ground with citations
- Avoids hallucination by using actual document content
- Citations show where answer came from

### 4. **Local LLM Integration**
- Ollama runs inference locally (no API calls)
- Privacy-first: data never leaves your machine
- Cost-effective: no per-token fees

### 5. **Metrics & Evaluation**
- Track latency (how fast responses are)
- Measure citation coverage (how well grounded)
- Analyze retrieval quality (top-k accuracy)

## 🔧 Configuration

### Backend (.env)
```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API=http://localhost:8000
```

## 📊 Usage Examples

### Query the Assistant
```bash
curl "http://localhost:8000/ask?q=What%20is%20our%20leave%20policy"
```

### Get Metrics
```bash
curl http://localhost:8000/metrics | jq .stats
```

### Upload & Reindex
```bash
# Upload a new document
curl -F "file=@company-handbook.pdf" http://localhost:8000/upload

# Rebuild index
curl -X POST http://localhost:8000/reindex
```

## 🧪 Testing

### Add Evaluation Questions
Edit `tools/eval.py` to add test questions:

```python
eval_questions = [
    "How many leave days do employees get?",
    "What is the remote work policy?",
    "How do I deploy to production?"
]
```

### Run Evaluation
```bash
python tools/eval.py
```

## 🚀 Production Deployment

### Azure
- **Frontend**: Azure Static Web Apps
- **Backend**: Azure App Service + Azure Cognitive Search
- **LLM**: Azure OpenAI API

### AWS
- **Frontend**: CloudFront + S3
- **Backend**: Lambda (serverless) or EC2
- **LLM**: SageMaker or Bedrock

### Docker (Local)
```bash
docker-compose up
```

## 🔐 Security Best Practices

- [ ] Store secrets in `.env` (never commit)
- [ ] Use HTTPS in production
- [ ] Implement API key authentication
- [ ] Sanitize user inputs
- [ ] Log sensitive data redaction (emails, IDs)
- [ ] Rate limit API endpoints

## 📈 Performance Tuning

### Latency Optimization
- Reduce chunk size for faster retrieval
- Use smaller embedding model (`MiniLM` vs `large`)
- Cache frequently accessed documents

### Accuracy Improvements
- Increase `k` in search (retrieve top-10 instead of top-5)
- Add reranking with cross-encoder
- Fine-tune embedding model on domain data

### Memory Optimization
- Use quantized models (4-bit, 8-bit)
- Stream large responses
- Batch process documents

## 📚 Learning Resources

### Understanding RAG
- [RAG Explained](https://docs.langchain.com/en/latest/modules/chains/index_related_chains/retrieval_qa.html)
- [Vector Databases](https://www.pinecone.io/learn/vector-database/)

### Embeddings
- [Sentence-Transformers](https://www.sbert.net/)
- [Embedding Models Comparison](https://huggingface.co/spaces/mteb/leaderboard)

### LLMs
- [Ollama Documentation](https://ollama.ai)
- [LLM Fine-tuning](https://huggingface.co/docs/peft)

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and test locally
3. Submit a pull request

## 📝 License

MIT - See LICENSE file for details

## ❓ FAQ

**Q: Can I use a cloud LLM instead of Ollama?**  
A: Yes! Edit `rag.py` to call Azure OpenAI, AWS Bedrock, or Anthropic instead.

**Q: How do I add custom documents?**  
A: Place Markdown/PDF/DOCX files in `data/raw/`, then run `python tools/reindex.py`

**Q: What if Ollama is offline?**  
A: The `/ask` endpoint will return an error. Ensure `ollama serve` is running.

**Q: How do I improve answer quality?**  
A: Try a larger model (`mistral`, `llama2`), increase retrieval context, or add document metadata.

**Q: Can I export chat history?**  
A: Frontend stores chat in localStorage. Export via download button (in development).

---

**Built with ❤️ for engineering onboarding and AI education**
