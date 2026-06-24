import re

def clean_text(text):
    # Remove 3+ consecutive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Remove extra spaces
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of ~chunk_size words.
    overlap = how many words carry over to the next chunk
    so context is not lost at boundaries.
    """
    words = text.split()
    chunks = []
    i = 0

    while i < len(words):
        chunk_words = words[i : i + chunk_size]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
        i += chunk_size - overlap  # move forward, keeping overlap words

    return chunks