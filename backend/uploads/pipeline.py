import os
import json
from core.ingestion.parsers import load_document
from core.ingestion.chunker import clean_text, chunk_text

def ingest_folder(folder="data/raw"):
    """
    Reads every document in the folder.
    For each document, cleans and chunks the text.
    Returns a list of chunk dicts ready for embedding.
    """
    all_chunks = []
    files = os.listdir(folder)

    for fname in files:
        # Skip JSON metadata files — they are not documents
        if fname.endswith(".json"):
            continue

        file_path = os.path.join(folder, fname)

        # Look for a matching .json metadata file
        base = os.path.splitext(fname)[0]
        meta_path = os.path.join(folder, base + ".json")

        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
        else:
            meta = {"title": fname, "type": "unknown", "tags": []}

        # Parse the document text
        raw_text = load_document(file_path)
        if not raw_text.strip():
            print(f"Skipping empty file: {fname}")
            continue

        # Clean and chunk
        clean = clean_text(raw_text)
        chunks = chunk_text(clean, chunk_size=500, overlap=50)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{base}_chunk_{i}"
            all_chunks.append({
                "id":     chunk_id,
                "text":   chunk,
                "source": fname,
                "meta":   meta
            })

        print(f"Processed: {fname} → {len(chunks)} chunk(s)")

    print(f"\nTotal chunks ready: {len(all_chunks)}")
    return all_chunks


if __name__ == "__main__":
    chunks = ingest_folder("data/raw")
    # Print a preview of the first chunk
    if chunks:
        print("\n--- Preview of first chunk ---")
        print(f"ID     : {chunks[0]['id']}")
        print(f"Source : {chunks[0]['source']}")
        print(f"Title  : {chunks[0]['meta'].get('title')}")
        print(f"Text   : {chunks[0]['text'][:300]}...")