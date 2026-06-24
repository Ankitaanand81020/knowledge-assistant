"""
Logging and metrics collection for RAG pipeline.
Tracks latency, retrieval quality, and citation coverage.
"""

from pathlib import Path
import json
from typing import List, Dict
from datetime import datetime


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

METRICS_LOG = LOG_DIR / "metrics.json"
QUERY_LOG = LOG_DIR / "queries.jsonl"

if not METRICS_LOG.exists():
    METRICS_LOG.write_text(json.dumps({"queries": []}, indent=2))


def save_metric(
    question: str,
    answer: str,
    latency: float,
    retrieved_docs: List[str],
    citations: List[Dict] = None
) -> None:
    """
    Log a complete query-response cycle.
    
    Args:
        question: User question
        answer: Generated answer
        latency: Response time in ms
        retrieved_docs: List of retrieved document sources
        citations: Citation metadata
    """
    data = load_metrics()
    
    metric = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer[:200],  # First 200 chars
        "latency_ms": latency,
        "retrieved_count": len(retrieved_docs),
        "retrieved_sources": retrieved_docs,
        "citation_count": len(citations) if citations else 0,
        "citations": citations or []
    }
    
    data["queries"].append(metric)
    METRICS_LOG.write_text(json.dumps(data, indent=2))


def load_metrics() -> Dict:
    """
    Load all metrics from log file.
    
    Returns:
        Dictionary with 'queries' list
    """
    try:
        content = METRICS_LOG.read_text()
        data = json.loads(content)
        return data if isinstance(data, dict) and "queries" in data else {"queries": []}
    except:
        return {"queries": []}


def get_stats() -> Dict:
    """
    Compute aggregate statistics on logged queries.
    
    Returns:
        Stats dict with avg_latency, total_queries, etc.
    """
    data = load_metrics()
    queries = data.get("queries", [])
    
    if not queries:
        return {
            "total_queries": 0,
            "avg_latency_ms": 0,
            "median_latency_ms": 0
        }
    
    latencies = [q.get("latency_ms", 0) for q in queries]
    latencies.sort()
    
    return {
        "total_queries": len(queries),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "median_latency_ms": latencies[len(latencies) // 2],
        "min_latency_ms": min(latencies),
        "max_latency_ms": max(latencies),
        "avg_citations": round(sum(q.get("citation_count", 0) for q in queries) / len(queries), 2)
    }