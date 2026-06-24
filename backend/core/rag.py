"""
Retrieval-Augmented Generation (RAG) pipeline.
Retrieves relevant context and generates grounded answers with citations.
"""

import httpx
import time
from datetime import datetime
from typing import List, Dict, Optional

from core.vector_store import search
from core.config import OLLAMA_URL, OLLAMA_MODEL
from core.logger import save_metric

# Relevance threshold: documents with distance > this are considered not relevant
# (lower distance = higher similarity in embedding space)
# Use a conservative default but also allow a relative-gap override so newly
# indexed documents that are much closer than others are still treated as
# relevant.
RELEVANCE_THRESHOLD = 1.5


def build_prompt(question: str, docs: List[Dict[str, str]]) -> tuple:
    """
    Build prompt with context and extract citations.
    
    Args:
        question: User question
        docs: Retrieved documents
    
    Returns:
        (prompt_text, citations_metadata)
    """
    context = "\n\n".join([f"[{i}] {d['text']}" for i, d in enumerate(docs)])
    citations = [{
        "id": i,
        "source": d.get("source", "unknown"),
        "text": d["text"][:100]
    } for i, d in enumerate(docs)]
    
    prompt = f"""You are an expert, professional AI Knowledge Assistant. Follow these rules exactly:
    - Use only the provided CONTEXT when explicitly citing facts; cite with [0], [1], etc.
    - Prefer answers based on the CONTEXT; if CONTEXT doesn't support a fact, say you don't know.
    - Be concise, factual, and professional. Do not hallucinate.
    - Provide a short, numbered list of key points when appropriate and include citations for claims drawn from the CONTEXT.
    - If the question requires general knowledge beyond the CONTEXT, label clearly which parts come from the CONTEXT and which are general knowledge.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""
    
    # Also return the raw context string so callers can reuse it for verification
    return prompt, citations, context


def build_fallback_prompt(question: str) -> str:
    """
    Build prompt for general questions when no documents are available.
    """
    return f"""You are an expert, professional AI assistant. Answer concisely and accurately. If unsure, say "I don't know" and provide best-effort general knowledge clearly labeled as such.

Question: {question}

Answer:"""


async def ask_llm(prompt: str, timeout: int = 60) -> str:
    """
    Call Ollama LLM synchronously.
    
    Args:
        prompt: Full prompt with context
    
    Returns:
        Generated answer
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.0  # deterministic for factual answers
                }
            )

            # Try to parse JSON safely
            try:
                data = response.json()
            except Exception:
                # non-JSON body
                body = await response.aread()
                text = body.decode("utf-8", errors="replace") if isinstance(body, (bytes, bytearray)) else str(body)
                return f"ERROR: LLM returned non-JSON response (status={response.status_code}): {text}"

            if response.status_code != 200:
                try:
                    err_data = response.json()
                    if isinstance(err_data, dict):
                        error_text = err_data.get("error") or err_data.get("detail") or err_data.get("message")
                        if error_text:
                            return f"ERROR: LLM returned status {response.status_code}: {error_text}"
                except Exception:
                    pass
                text = response.text
                return f"ERROR: LLM returned status {response.status_code}: {text}"

            if not isinstance(data, dict):
                return f"ERROR: LLM returned unexpected response type: {type(data)}"

            if "error" in data and data["error"]:
                return f"ERROR: {data['error']}"

            if not data.get("response"):
                return "ERROR: LLM returned empty response"

            return data.get("response", "")
    except httpx.ConnectError:
        return "ERROR: Cannot connect to Ollama. Is it running on " + OLLAMA_URL + "?"
    except Exception as e:
        return f"ERROR: {str(e)}"


async def ask(question: str) -> Dict:
    """
    Main RAG query function: retrieve, generate, cite.
    
    Args:
        question: User question
    
    Returns:
        Dict with answer, citations, and metadata
    """
    start = time.time()
    
    # Retrieve relevant documents (increase k to gather more evidence)
    docs = search(question, k=8)
    
    # Check relevance first before building prompt. Use a hybrid rule:
    # - Absolute threshold (`RELEVANCE_THRESHOLD`) for typical similarity check
    # - Relative gap: if the top doc is substantially closer than the 2nd doc,
    #   treat it as relevant (covers freshly indexed docs where absolute
    #   distances may vary)
    distances = [d.get("distance", float('inf')) for d in docs]
    top_doc_distance = distances[0] if distances else float('inf')
    second_doc_distance = distances[1] if len(distances) > 1 else float('inf')

    is_relevant = False
    if top_doc_distance < RELEVANCE_THRESHOLD:
        is_relevant = True
    else:
        # If the top doc is noticeably closer than the next candidate, consider
        # it relevant (20% gap heuristic)
        try:
            if top_doc_distance <= 0.8 * second_doc_distance:
                is_relevant = True
        except Exception:
            is_relevant = False
    
    # If not relevant or no docs, answer from general knowledge
    if not is_relevant:
        prompt = build_fallback_prompt(question)
        citations = []
        sources = []
        try:
            answer = await ask_llm(prompt, timeout=60)
            if isinstance(answer, str) and answer.startswith("ERROR:"):
                # retry once with longer timeout
                answer = await ask_llm(prompt, timeout=120)
                if isinstance(answer, str) and answer.startswith("ERROR:"):
                    raise RuntimeError(answer)
        except Exception as llm_exc:
            print(f"LLM fallback error: {llm_exc}")
            answer = "I'm sorry, I couldn't generate an answer right now. Please try again later."
    else:
        # Build prompt with context from relevant documents
        prompt, citations, context = build_prompt(question, docs)
        try:
            answer = await ask_llm(prompt, timeout=60)
            if isinstance(answer, str) and answer.startswith("ERROR:"):
                # retry once with longer timeout
                answer = await ask_llm(prompt, timeout=120)
                if isinstance(answer, str) and answer.startswith("ERROR:"):
                    raise RuntimeError(answer)
            sources = [d.get("source", "unknown") for d in docs]
            sources = list(dict.fromkeys(sources))  # deduplicate while preserving order
        except Exception as llm_exc:
            print(f"LLM retrieval error: {llm_exc}")
            answer = "I'm sorry, I couldn't generate an answer right now. Please try again later."
            citations = []
            sources = []
        else:
            # Verify the generated answer is supported by the CONTEXT when documents were used.
            try:
                # Build a short verification prompt that asks the model to confirm whether
                # the provided answer is supported by the context. Expect a short token like
                # 'SUPPORTED' or 'NOT_SUPPORTED' at the start of the response.
                verify_prompt = f"""CONTEXT:
{context}

PROVIDED_ANSWER:
{answer}

QUESTION:
{question}

Task: Based only on the CONTEXT above, reply with either SUPPORTED or NOT_SUPPORTED, followed by one short sentence justification.
"""
                verification = await ask_llm(verify_prompt, timeout=30)
                if isinstance(verification, str) and verification.strip().upper().startswith("NOT_SUPPORTED"):
                    # If the answer is not supported by the retrieved context, fall back to a general-knowledge answer.
                    fb_prompt = build_fallback_prompt(question)
                    fb_answer = await ask_llm(fb_prompt, timeout=60)
                    if isinstance(fb_answer, str) and fb_answer.startswith("ERROR:"):
                        # retry fallback once
                        fb_answer = await ask_llm(fb_prompt, timeout=120)
                        if isinstance(fb_answer, str) and fb_answer.startswith("ERROR:"):
                            raise RuntimeError(fb_answer)
                    answer = fb_answer
                    citations = []
                    sources = []
            except Exception as verify_exc:
                # Verification failed; keep the original answer but log the issue.
                print(f"Answer verification error: {verify_exc}")

    latency = round((time.time() - start) * 1000, 2)
    try:
        save_metric(
            question=question,
            answer=answer,
            latency=latency,
            retrieved_docs=[d.get("source", "unknown") for d in (docs if is_relevant else [])],
            citations=citations
        )
    except Exception as e:
        print(f"Logging error: {e}")

    # Filter out corrupted/binary citations from the response
    clean_citations = []
    for cit in citations:
        text = cit.get("text", "")
        # Skip if text contains too many non-ASCII or control characters (binary data)
        non_ascii_ratio = sum(1 for c in text if ord(c) > 127 or (ord(c) < 32 and c not in "\n\t")) / max(len(text), 1)
        if non_ascii_ratio < 0.1:  # Allow < 10% non-ASCII
            clean_citations.append(cit)

    resp = {
        "question": question,
        "answer": answer,
        "citations": clean_citations if clean_citations else citations,
        "retrieved_count": len(docs) if is_relevant else 0,
        "sources": sources,
        "timestamp": datetime.now().isoformat(),
        "latency_ms": latency,
    }

    return resp


async def ask_stream(question: str):
    """
    Stream RAG response for real-time feedback.
    
    Args:
        question: User question
    
    Yields:
        Text chunks as they're generated
    """
    docs = search(question, k=5)
    
    if not docs:
        yield "No relevant documents found in the knowledge base."
        return
    
    prompt, _, _ = build_prompt(question, docs)
    
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": True,
                    "temperature": 0.3
                }
            ) as res:
                async for line in res.aiter_lines():
                    if line:
                        try:
                            import json
                            chunk = json.loads(line)
                            if "response" in chunk:
                                yield chunk["response"]
                        except:
                            pass
    except Exception as e:
        yield f"ERROR: {str(e)}"