import sys
import os

# Make sure Python can find the core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ingestion.pipeline import ingest_folder
from core.embeddings.vector_store import index_chunks, get_collection_count

print("=" * 50)
print("  AI Knowledge Assistant — Index Builder")
print("=" * 50)

# Step 1: Ingest all documents from data/raw
print("\nStep 1: Ingesting documents from data/raw...")
chunks = ingest_folder("data/raw")

if not chunks:
    print("No chunks found. Make sure data/raw has documents.")
    sys.exit(1)

# Step 2: Embed and store in ChromaDB
print("\nStep 2: Embedding and storing in ChromaDB...")
index_chunks(chunks)

# Step 3: Confirm
count = get_collection_count()
print("\n" + "=" * 50)
print(f"  Index built successfully!")
print(f"  Total chunks in database: {count}")
print("=" * 50)