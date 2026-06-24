"""
Reindexing script: Load documents, chunk them, and index into Chroma.
Run this after adding new documents or updating configuration.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ingestion import ingest_documents
from core.vector_store import add_chunks, clear_db, get_collection_count


BASE_DIR = Path(__file__).resolve().parent.parent


def resolve_folder(folder: str) -> str:
    """Resolve folder path relative to backend root."""
    path = Path(folder)
    if not path.is_absolute():
        path = BASE_DIR / folder
    return str(path)


def reindex(folders=None, chunk_size: int = 500, overlap: int = 100):
    """
    Full reindex pipeline: load, chunk, and index documents from one or more folders.
    
    Args:
        folders: List of folders to index
        chunk_size: Words per chunk
        overlap: Word overlap between chunks
    """
    if folders is None:
        folders = ["data/raw", "uploads"]

    print("[REINDEX] Starting reindex pipeline...")

    # Clear existing index
    print("[REINDEX] Clearing existing vector store...")
    clear_db()

    all_chunks = []
    for folder in folders:
        resolved_folder = resolve_folder(folder)
        print(f"[REINDEX] Ingesting documents from {resolved_folder}...")
        chunks = ingest_documents(resolved_folder, chunk_size, overlap, normalize=True)
        all_chunks.extend(chunks)

    if not all_chunks:
        print("[REINDEX] No documents found to index!")
        return False

    # Index chunks
    print(f"[REINDEX] Indexing {len(all_chunks)} chunks...")

    # Group chunks by source for efficient indexing
    sources = {}
    for chunk in all_chunks:
        source = chunk.get("source", "unknown")
        if source not in sources:
            sources[source] = []
        sources[source].append(chunk["text"])

    # Add to vector store
    for source, chunk_texts in sources.items():
        add_chunks(chunk_texts, source=source)

    # Verify
    count = get_collection_count()
    print("[REINDEX] Reindexing complete!")
    print(f"[REINDEX] Documents in index: {count}")
    print(f"[REINDEX] Unique sources: {len(sources)}")

    return True


def reindex_all(chunk_size: int = 500, overlap: int = 100):
    """
    Reindex both data/raw and uploads folders.
    """
    return reindex(["data/raw", "uploads"], chunk_size, overlap)


if __name__ == "__main__":
    reindex()