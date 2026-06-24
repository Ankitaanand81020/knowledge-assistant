import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.embeddings.vector_store import search

# Test questions — these should match your synthetic documents
test_questions = [
    "What is the leave policy?",
    "When is payday?",
    "How do I connect to the VPN?",
    "What are the coding best practices?",
]

for question in test_questions:
    print("\n" + "=" * 50)
    print(f"Question: {question}")
    print("=" * 50)

    results = search(question, top_k=2)

    docs      = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances)):
        score = round((1 - dist) * 100, 1)  # convert distance to similarity %
        print(f"\n  Result {i+1}")
        print(f"  Source    : {meta['source']}")
        print(f"  Title     : {meta['title']}")
        print(f"  Similarity: {score}%")
        print(f"  Text      : {doc[:200]}...")