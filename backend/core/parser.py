"""
Document parsers for multiple formats.
Supports Markdown, PDF, DOCX, CSV, TXT.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


def parse_markdown(file_path: str) -> Dict[str, str]:
    """Parse Markdown file."""
    text = Path(file_path).read_text(encoding="utf-8")
    return {
        "text": text,
        "source": Path(file_path).name,
        "type": "markdown"
    }


def parse_json(file_path: str) -> Dict[str, str]:
    """Parse JSON file (assumes content/text key exists)."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Handle JSON that may be an object or an array
    if isinstance(data, dict):
        text = data.get("content") or data.get("text") or json.dumps(data)
        title = data.get("title", "")
        tags = data.get("tags", [])
    else:
        # For lists or other JSON structures, store the serialized JSON
        text = json.dumps(data)
        title = ""
        tags = []

    return {
        "text": text,
        "source": Path(file_path).name,
        "type": "json",
        "title": title,
        "tags": tags,
    }


def parse_txt(file_path: str) -> Dict[str, str]:
    """Parse plain text file."""
    text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    return {
        "text": text,
        "source": Path(file_path).name,
        "type": "text"
    }


def parse_pdf(file_path: str) -> Dict[str, str]:
    """Parse PDF file using PyMuPDF."""
    try:
        import fitz
    except ImportError:
        raise ImportError("PyMuPDF not installed. Install with: pip install PyMuPDF")
    
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    
    return {
        "text": text,
        "source": Path(file_path).name,
        "type": "pdf"
    }


def parse_html(file_path: str) -> Dict[str, str]:
    """Parse HTML file by extracting visible text."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        # Fallback: return raw file text if bs4 not installed
        text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        return {"text": text, "source": Path(file_path).name, "type": "html"}

    html = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    # Get visible text
    for script in soup(["script", "style"]):
        script.extract()
    text = "\n".join([s.strip() for s in soup.stripped_strings])

    return {"text": text, "source": Path(file_path).name, "type": "html"}


def parse_docx(file_path: str) -> Dict[str, str]:
    """Parse DOCX file."""
    try:
        from docx import Document
    except ImportError:
        raise ImportError("python-docx not installed. Install with: pip install python-docx")
    
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    
    return {
        "text": text,
        "source": Path(file_path).name,
        "type": "docx"
    }


def parse_doc(file_path: str) -> Dict[str, str]:
    """Parse legacy .doc files using unstructured."""
    try:
        from unstructured.partition.auto import partition
    except ImportError:
        raise ImportError("unstructured not installed. Install with: pip install unstructured")

    elements = partition(filename=file_path)
    text = "\n\n".join([str(el) for el in elements])

    return {
        "text": text,
        "source": Path(file_path).name,
        "type": "doc"
    }


def parse_csv(file_path: str) -> Dict[str, str]:
    """Parse CSV file."""
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas not installed. Install with: pip install pandas")
    
    df = pd.read_csv(file_path)
    text = df.to_string(index=False)
    
    return {
        "text": text,
        "source": Path(file_path).name,
        "type": "csv"
    }


def parse_code(file_path: str) -> Dict[str, str]:
    """Parse source code and other plain-text file types."""
    text = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    return {"text": text, "source": Path(file_path).name, "type": "code"}


def parse_unknown(file_path: str) -> Optional[Dict[str, str]]:
    """Attempt to parse unknown/binary files by trying text decodes.

    If the file cannot be decoded as text, return a short placeholder message
    indicating the file name so that uploads do not get silently skipped.
    """
    p = Path(file_path)
    try:
        # Try utf-8 then latin-1
        text = p.read_text(encoding="utf-8")
        return {"text": text, "source": p.name, "type": "unknown"}
    except Exception:
        try:
            text = p.read_text(encoding="latin-1")
            return {"text": text, "source": p.name, "type": "unknown"}
        except Exception:
            # Binary file; return minimal metadata so the file is indexed with its filename
            return {"text": f"[Non-text file: {p.name}]. Content not extracted.", "source": p.name, "type": "binary"}


def parse_document(file_path: str) -> Optional[Dict[str, str]]:
    """
    Auto-detect file type and parse accordingly.
    
    Args:
        file_path: Path to document
    
    Returns:
        Dictionary with parsed text and metadata
    """
    file_path = str(file_path)
    extension = Path(file_path).suffix.lower()
    
    parsers = {
        ".md": parse_markdown,
        ".txt": parse_txt,
        ".json": parse_json,
        ".pdf": parse_pdf,
        ".docx": parse_docx,
        ".doc": parse_doc,
        ".csv": parse_csv,
        ".html": parse_html,
        ".htm": parse_html,
        # common code/text file extensions
        ".py": parse_code,
        ".java": parse_code,
        ".js": parse_code,
        ".ts": parse_code,
        ".jsx": parse_code,
        ".tsx": parse_code,
        ".xml": parse_code,
        ".yaml": parse_code,
        ".yml": parse_code,
    }
    
    parser = parsers.get(extension)
    if not parser:
        # Fallback: attempt to extract text from unknown files
        return parse_unknown(file_path)
    
    try:
        return parser(file_path)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def parse_folder(folder_path: str, extensions: Optional[List[str]] = None) -> List[Dict[str, str]]:
    """
    Parse all documents in a folder.
    
    Args:
        folder_path: Path to folder
        extensions: List of extensions to parse (e.g., ['.md', '.pdf']). None = all supported.
    
    Returns:
        List of parsed documents
    """
    folder = Path(folder_path)
    documents = []
    
    if extensions is None:
        # Walk all files in folder and attempt to parse each one using parse_document
        for file_path in folder.rglob("*"):
            if file_path.is_file():
                doc = parse_document(str(file_path))
                if doc:
                    documents.append(doc)
    else:
        for ext in extensions:
            for file_path in folder.rglob(f"*{ext}"):
                doc = parse_document(str(file_path))
                if doc:
                    documents.append(doc)
    
    return documents