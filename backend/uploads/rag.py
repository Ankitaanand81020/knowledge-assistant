import httpx
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.embeddings.vector_store import search

# Ollama config
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"


def build_prompt(question: str, context_chunks: list) -> str:
    """
    Build prompt with retrieved context
    """
    context = "\n\n---\n\n".join(context_chunks) if context_chunks else ""

    prompt = f"""
You are a helpful internal knowledge assistant.

Rules:
- Use ONLY the provided context.
- If answer is not in context, say: "I don't have enough information in my knowledge base."
- Be clear and concise.

--- CONTEXT START ---
{context}
--- CONTEXT END ---

Question: {question}

Answer:
"""
    return prompt


def ask(question: str, top_k: int = 5) -> dict:
    """
    Full RAG pipeline:
    1. Retrieve relevant chunks
    2. Build prompt
    3. Call Ollama
    4. Return answer + citations
    """

    # ----------------------------
    # Step 1: Retrieve documents
    # ----------------------------
    results = search(question, top_k=top_k)

    documents = results.get("documents", [[]])[0] if results.get("documents") else []
    metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []
    distances = results.get("distances", [[]])[0] if results.get("distances") else []

    # ----------------------------
    # Step 2: Handle empty results
    # ----------------------------
    if not documents:
        return {
            "answer": "No relevant documents found in the knowledge base.",
            "citations": []
        }

    # ----------------------------
    # Step 3: Build prompt
    # ----------------------------
    prompt = build_prompt(question, documents)

    # ----------------------------
    # Step 4: Call Ollama
    # ----------------------------
    try:
        response = httpx.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 512
                }
            },
            timeout=120
        )

        response.raise_for_status()
        answer = response.json().get("response", "").strip()

    except httpx.ConnectError:
        return {
            "answer": "Cannot connect to Ollama. Make sure 'ollama serve' is running.",
            "citations": []
        }

    except Exception as e:
        return {
            "answer": f"Error generating answer: {str(e)}",
            "citations": []
        }

    # ----------------------------
    # Step 5: Build citations safely
    # ----------------------------
    citations = []

    for i in range(len(documents)):
        meta = metadatas[i] if i < len(metadatas) else {}
        dist = distances[i] if i < len(distances) else 1.0

        similarity = round((1 - dist) * 100, 1)

        citations.append({
            "source": meta.get("source", "unknown"),
            "title": meta.get("title", "unknown"),
            "type": meta.get("type", "unknown"),
            "similarity": similarity
        })

    return {
        "answer": answer,
        "citations": citations
    }


# ----------------------------
# Local test
# ----------------------------
if __name__ == "__main__":
    test_q = "What is the annual leave entitlement?"

    print(f"\nQuestion: {test_q}\n")

    result = ask(test_q)

    print("Answer:\n")
    print(result["answer"])

    print("\nCitations:")
    for c in result["citations"]:
        print(f"- {c['title']} ({c['source']}) — {c['similarity']}% match")