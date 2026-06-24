#!/usr/bin/env python3
"""
Evaluation script for Knowledge Assistant.
Tests the system with sample questions and measures performance.
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

from core.rag import ask
from core.logger import load_metrics, get_stats


# Sample evaluation questions across different categories
EVAL_QUESTIONS = [
    # HR / Policies
    "How many vacation days do employees get?",
    "What is the remote work policy?",
    "How do I request leave?",
    
    # Technical
    "How do I set up the development environment?",
    "What are the API authentication methods?",
    "How do I deploy to production?",
    
    # Onboarding
    "What happens on my first day?",
    "Who should I meet during onboarding?",
    
    # General
    "How do I report a bug?",
    "Who is the CTO?",
]


async def evaluate():
    """Run evaluation suite on sample questions."""
    print("\n" + "="*60)
    print("📊 Knowledge Assistant Evaluation")
    print("="*60 + "\n")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "questions_tested": len(EVAL_QUESTIONS),
        "results": []
    }
    
    for i, question in enumerate(EVAL_QUESTIONS, 1):
        print(f"[{i}/{len(EVAL_QUESTIONS)}] {question}")
        
        try:
            response = await ask(question)
            
            result = {
                "question": question,
                "answer_length": len(response.get("answer", "")),
                "latency_ms": response.get("latency_ms", 0),
                "citations": len(response.get("citations", [])),
                "sources": response.get("sources", []),
                "status": "✅ Success"
            }
            
            print(f"  Latency: {result['latency_ms']}ms")
            print(f"  Citations: {result['citations']}")
            print()
            
            results["results"].append(result)
            
        except Exception as e:
            result = {
                "question": question,
                "status": f"❌ Error: {str(e)}"
            }
            print(f"  Error: {str(e)}\n")
            results["results"].append(result)
    
    # Compute statistics
    successful = [r for r in results["results"] if "Success" in r.get("status", "")]
    
    if successful:
        latencies = [r["latency_ms"] for r in successful]
        citations = [r["citations"] for r in successful]
        
        results["stats"] = {
            "success_rate": f"{len(successful)/len(EVAL_QUESTIONS)*100:.1f}%",
            "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "avg_citations": round(sum(citations) / len(citations), 1),
        }
        
        print("\n" + "="*60)
        print("📈 Results Summary")
        print("="*60)
        for key, value in results["stats"].items():
            print(f"{key:.<40} {value}")
    
    # Save results
    eval_dir = Path("data/evaluations")
    eval_dir.mkdir(exist_ok=True)
    
    eval_file = eval_dir / f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    eval_file.write_text(json.dumps(results, indent=2))
    
    print(f"\n✅ Evaluation saved to {eval_file}")


if __name__ == "__main__":
    asyncio.run(evaluate())
