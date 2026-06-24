"""
Text chunking utilities for RAG pipeline.
Supports configurable chunk sizes with optional overlap.
"""

from typing import List, Dict


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> List[str]:
    """
    Split text into overlapping chunks by word count.
    
    Args:
        text: Text to chunk
        chunk_size: Target words per chunk
        overlap: Overlap between chunks (words)
    
    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []
    
    i = 0
    while i < len(words):
        end = min(i + chunk_size, len(words))
        chunk = " ".join(words[i:end])
        chunks.append(chunk)

        if end == len(words):
            break

        next_i = end - overlap if overlap > 0 else end
        if next_i <= i:
            next_i = i + 1
        i = next_i

    return chunks

def chunk_documents(
    documents: List[Dict[str, str]],
    chunk_size: int = 500,
    overlap: int = 100,
) -> List[Dict[str, str]]:
    """
    Chunk multiple documents while preserving metadata.
    
    Args:
        documents: List of dicts with 'text' and 'source' keys
        chunk_size: Target words per chunk
        overlap: Overlap between chunks
    
    Returns:
        List of chunked documents with preserved metadata
    """
    chunked = []
    
    for doc in documents:
        text = doc.get("text", "")
        source = doc.get("source", "unknown")
        chunks = chunk_text(text, chunk_size, overlap)
        
        for i, chunk in enumerate(chunks):
            chunked.append({
                "text": chunk,
                "source": source,
                "chunk_id": i,
                "title": doc.get("title", ""),
                "tags": doc.get("tags", []),
            })
    
    return chunked