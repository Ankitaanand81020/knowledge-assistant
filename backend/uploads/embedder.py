from sentence_transformers import SentenceTransformer

# Load the model once when this module is imported
# all-MiniLM-L6-v2 is fast, small (~80MB), and works great for English text
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded.")

def embed_texts(texts: list) -> list:
    """
    Takes a list of strings.
    Returns a list of embedding vectors (one per string).
    """
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    return embeddings.tolist()