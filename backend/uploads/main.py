import sys
import os
import time
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from core.retrieval.rag import ask
from core.ingestion.pipeline import ingest_folder
from core.embeddings.vector_store import index_chunks, get_collection_count
from core.security import redact_pii, is_safe_question, sanitize_input
from core.config import API_TOKEN, LOG_PATH

app = FastAPI(
    title="AI Knowledge Assistant API",
    description="RAG-based internal knowledge assistant using Qwen2.5 + ChromaDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Checks the Bearer token in the Authorization header.
    Skips check if API_TOKEN is not set in .env (dev mode).
    """
    if not API_TOKEN:
        return True  # No token configured — allow all (dev mode)
    if credentials is None or credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing API token.")
    return True


# ---------- Models ----------

class QuestionRequest(BaseModel):
    question: str
    top_k:    int = 5

class AnswerResponse(BaseModel):
    answer:     str
    citations:  list
    latency_ms: int
    question:   str
    pii_found:  list


# ---------- Routes ----------

@app.get("/")
def root():
    return {
        "status":         "running",
        "model":          "qwen2.5:1.5b",
        "chunks_indexed": get_collection_count(),
        "auth":           "enabled" if API_TOKEN else "disabled (dev mode)"
    }


@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest, authorized: bool = Depends(verify_token)):

    # Sanitize input
    question = sanitize_input(req.question)

    # Safety check
    safe, reason = is_safe_question(question)
    if not safe:
        raise HTTPException(status_code=400, detail=reason)

    # Redact any PII in the question before it hits the LLM
    clean_question, pii_found = redact_pii(question)
    if pii_found:
        print(f"PII detected and redacted in question: {pii_found}")

    start_time = time.time()
    result     = ask(clean_question, top_k=req.top_k)
    latency_ms = round((time.time() - start_time) * 1000)

    # Log query
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp":   time.strftime("%Y-%m-%dT%H:%M:%S"),
        "question":    clean_question,
        "answer":      result["answer"],
        "citations":   result["citations"],
        "latency_ms":  latency_ms,
        "pii_found":   pii_found
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {
        "answer":     result["answer"],
        "citations":  result["citations"],
        "latency_ms": latency_ms,
        "question":   clean_question,
        "pii_found":  pii_found
    }


@app.post("/reindex")
def reindex(authorized: bool = Depends(verify_token)):
    try:
        chunks = ingest_folder("data/raw")
        index_chunks(chunks)
        return {"status": "success", "chunks_indexed": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
def stats():
    if not os.path.exists(LOG_PATH):
        return {"total_queries": 0, "average_latency_ms": 0, "pii_detections": 0}

    queries = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                queries.append(json.loads(line))

    avg_latency    = round(sum(q["latency_ms"] for q in queries) / len(queries)) if queries else 0
    pii_detections = sum(1 for q in queries if q.get("pii_found"))

    return {
        "total_queries":    len(queries),
        "average_latency_ms": avg_latency,
        "pii_detections":   pii_detections,
        "last_query":       queries[-1]["question"] if queries else None
    }
