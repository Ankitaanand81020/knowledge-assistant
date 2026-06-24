import os
import fitz          # PyMuPDF — reads PDF
import docx2txt      # reads DOCX
import pandas as pd  # reads CSV

def parse_md(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def parse_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_docx(path):
    return docx2txt.process(path)

def parse_csv(path):
    df = pd.read_csv(path)
    return df.to_string(index=False)

def load_document(path):
    ext = path.split(".")[-1].lower()
    parsers = {
        "md":   parse_md,
        "pdf":  parse_pdf,
        "docx": parse_docx,
        "csv":  parse_csv,
    }
    parser = parsers.get(ext)
    if parser is None:
        print(f"Skipping unsupported file: {path}")
        return ""
    try:
        return parser(path)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""