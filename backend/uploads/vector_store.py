import chromadb
from core.embeddings.embedder import embed_texts

# ChromaDB will save data to this folder on disk
# So your index survives restarts
CHROMA_PATH = "data/chroma_db"
COLLECTION_NAME = "knowledge_base"

# Create a persistent client
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Get or create the collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}  # cosine similarity
)


def index_chunks(chunks: list):
    """
    Takes a list of chunk dicts from the ingestion pipeline.
    Generates embeddings and stores everything in ChromaDB.
    """
    if not chunks:
        print("No chunks to index.")
        return

    ids        = [c["id"] for c in chunks]
    texts      = [c["text"] for c in chunks]
    metadatas  = []

    for c in chunks:
        meta = {
            "source": c["source"],
            "title":  c["meta"].get("title", ""),
            "type":   c["meta"].get("type", ""),
            "tags":   ", ".join(c["meta"].get("tags", [])),
        }
        metadatas.append(meta)

    print(f"\nGenerating embeddings for {len(texts)} chunks...")
    embeddings = embed_texts(texts)

    # Delete existing entries to avoid duplicates on re-index
    existing = collection.get(ids=ids)
    existing_ids = existing["ids"]
    if existing_ids:
        collection.delete(ids=existing_ids)
        print(f"Removed {len(existing_ids)} old entries before re-indexing.")

    # Add to ChromaDB
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Successfully indexed {len(chunks)} chunks into ChromaDB.")
    print(f"Database saved at: {CHROMA_PATH}")


def search(query: str, top_k: int = 5) -> dict:
    """
    Takes a natural language query.
    Returns the top_k most relevant chunks from the vector store.
    """
    print(f"\nSearching for: '{query}'")
    query_embedding = embed_texts([query])

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results


def get_collection_count() -> int:
    return collection.count()