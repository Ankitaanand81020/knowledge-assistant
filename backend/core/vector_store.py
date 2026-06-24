"""
Vector store for embeddings using Chroma.
Handles indexing and semantic search.
"""
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Lazy-loaded module state to avoid heavy imports at import-time
_model = None
_client = None
_collection = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def get_client():
    global _client
    if _client is None:
        db_path = BASE_DIR.parent / "data" / "chroma_db"
        _client = chromadb.PersistentClient(path=str(db_path))
    return _client


def get_collection():
    global _collection
    if _collection is None:
        _collection = get_client().get_or_create_collection("knowledge")
    return _collection


def add_chunks(chunks: List[str], source: str = "unknown", metadata: Dict = None) -> None:
    """
    Add chunked documents to vector store.
    
    Args:
        chunks: List of text chunks
        source: Document source identifier
        metadata: Additional metadata dict
    """
    col = get_collection()
    model = get_model()
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue

        emb = model.encode(chunk).tolist()

        chunk_meta = {"source": source, "chunk_index": i}
        if metadata:
            chunk_meta.update(metadata)

        col.add(
            ids=[f"{source}_{i}"],
            embeddings=[emb],
            documents=[chunk],
            metadatas=[chunk_meta]
        )




def search(query: str, k: int = 5) -> List[Dict[str, str]]:
    """
    Search for relevant documents using semantic similarity.
    
    Args:
        query: User query
        k: Number of results to return
    
    Returns:
        List of dicts with 'text', 'source', 'distance' keys
    """
    try:
        model = get_model()
        q_emb = model.encode(query).tolist()
    except Exception as e:
        print(f"Encoding error: {e}")
        return []

    try:
        col = get_collection()
        result = col.query(
            query_embeddings=[q_emb],
            n_results=k
        )
    except Exception as e:
        print(f"Search error: {e}")
        return []
    # Guard against unexpected return types from the collection/query
    if not result or not isinstance(result, dict):
        print(f"Search warning: unexpected query result: {result}")
        return []

    if not result.get("documents") or not result["documents"][0]:
        return []
    
    docs = result["documents"][0]
    metas = result["metadatas"][0]
    distances = result.get("distances", [[]])[0]
    
    output = []
    for doc, meta, dist in zip(docs, metas, distances):
        output.append({
            "text": doc,
            "source": meta.get("source", "unknown"),
            "chunk_index": meta.get("chunk_index", 0),
            "distance": dist
        })
    
    return output


def clear_db() -> None:
    """Clear all documents from vector store."""
    try:
        col = get_collection()
        # Get all IDs and delete them
        all_items = col.get()
        if all_items and all_items.get("ids"):
            col.delete(ids=all_items["ids"])
    except Exception as e:
        print(f"Error clearing collection: {e}")


def get_collection_count() -> int:
    """Get number of documents in collection."""
    try:
        col = get_collection()
        return col.count()
    except Exception:
        return 0