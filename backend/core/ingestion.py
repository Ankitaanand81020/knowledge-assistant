"""
Document ingestion pipeline for the knowledge base.
Loads, normalizes, and chunks documents for indexing.
"""

from pathlib import Path
from typing import List, Dict
from core.parser import parse_folder
from core.chunking import chunk_documents


def load_documents(folder: str = "data/raw") -> List[Dict[str, str]]:
    """
    Load all documents from a folder using auto-detection.
    
    Args:
        folder: Path to document folder
    
    Returns:
        List of parsed document dictionaries
    """
    print(f"Loading documents from {folder}...")
    documents = parse_folder(folder)
    print(f"Loaded {len(documents)} documents")
    return documents


def normalize_text(text: str) -> str:
    """
    Clean and normalize document text.
    
    Args:
        text: Raw text
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = " ".join(text.split())
    # Remove common markdown markers (if not already done by parser)
    text = text.replace("#", "").replace("*", "")
    return text


def ingest_documents(
    folder: str = "data/raw",
    chunk_size: int = 500,
    overlap: int = 100,
    normalize: bool = True
) -> List[Dict[str, str]]:
    """
    Complete ingestion pipeline: load, normalize, chunk.
    
    Args:
        folder: Document folder path
        chunk_size: Words per chunk
        overlap: Word overlap between chunks
        normalize: Whether to clean text
    
    Returns:
        List of chunks with metadata
    """
    # Load documents
    documents = load_documents(folder)
    
    # Normalize if requested
    if normalize:
        for doc in documents:
            doc["text"] = normalize_text(doc["text"])
    
    # Chunk documents
    chunks = chunk_documents(documents, chunk_size, overlap)
    print(f"Created {len(chunks)} chunks from {len(documents)} documents")
    
    return chunks