"""
API routes for the Knowledge Assistant.
Handles queries, exports, reindexing, and metrics.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
import shutil
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, Any
from zipfile import ZipFile

from core.rag import ask
from core.exporter import export_docx, export_xlsx
from core.logger import load_metrics, get_stats

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

router = APIRouter()



@router.get("/ask")
async def query(q: str) -> Dict[str, Any]:
    """
    Main query endpoint: retrieve docs and generate answer with citations.
    
    Args:
        q: User question
    
    Returns:
        JSON with answer, citations, latency, sources
    """
    if not q or len(q.strip()) < 3:
        raise HTTPException(status_code=400, detail="Question too short")
    
    try:
        result = await ask(q)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")


@router.post("/export/docx")
async def export_doc(data: Dict[str, Any]) -> FileResponse:
    """
    Export answer to Word document.
    
    Args:
        data: Dict with 'question' and 'answer' keys
    
    Returns:
        DOCX file response
    """
    try:
        return export_docx(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


@router.post("/export/xlsx")
async def export_excel(data: Dict[str, Any]) -> FileResponse:
    """
    Export answer to Excel spreadsheet.
    
    Args:
        data: Dict with 'question' and 'answer' keys
    
    Returns:
        XLSX file response
    """
    try:
        return export_xlsx(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


@router.post("/upload")
async def upload(request: Request) -> Dict[str, Any]:
    """
    Upload one or more documents to the knowledge base.
    Files are saved to uploads/ and the vector store is rebuilt to include them.
    
    Args:
        files: List of document files
    
    Returns:
        Success message with uploaded file names
    """
    # Read form data and collect UploadFile instances from any field name
    form = await request.form()
    # Accept both FastAPI/Starlette UploadFile or any file-like form field
    files = []
    for v in form.values():
        if isinstance(v, UploadFile):
            files.append(v)
        else:
            # fallback duck-typing: has filename and file-like
            if hasattr(v, "filename") and hasattr(v, "file"):
                files.append(v)

    if not files:
        raise HTTPException(status_code=400, detail="No files provided in form data")

    uploaded_files = []
    try:
        for file in files:
            try:
                if not file.filename:
                    continue

                safe_name = os.path.basename(file.filename)
                path = UPLOADS_DIR / safe_name
                with open(path, "wb") as f:
                    shutil.copyfileobj(file.file, f)
                uploaded_files.append(safe_name)

                if path.suffix.lower() == ".zip":
                    try:
                        with ZipFile(path, "r") as zip_ref:
                            zip_ref.extractall(UPLOADS_DIR)
                    except Exception as zip_exc:
                        # continue processing other files but note the error
                        raise HTTPException(status_code=500, detail=f"Zip extraction failed for {safe_name}: {zip_exc}")
            finally:
                try:
                    await file.close()
                except Exception:
                    pass

        # Rebuild the vector store to include uploaded documents.
        # Spawn reindex in background to avoid blocking upload with heavy imports
        try:
            subprocess.Popen([sys.executable, str(BASE_DIR / "tools" / "reindex.py")], cwd=str(BASE_DIR))
        except Exception as sub_exc:
            err_path = BASE_DIR / "logs" / "upload_error.log"
            os.makedirs(err_path.parent, exist_ok=True)
            with open(err_path, "a", encoding="utf-8") as ef:
                ef.write(f"Failed to spawn reindex subprocess: {sub_exc}\n")
            raise HTTPException(status_code=500, detail=f"Failed to start reindex: {sub_exc}")

        return {
            "message": "Files uploaded and indexed successfully",
            "filenames": uploaded_files,
            "status": "success"
        }
    except HTTPException:
        raise
    except Exception as e:
        # Write full exception for debugging
        err_path = BASE_DIR / "logs" / "upload_error.log"
        os.makedirs(err_path.parent, exist_ok=True)
        with open(err_path, "a", encoding="utf-8") as ef:
            ef.write(f"Unhandled upload error: {e}\n")
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")


@router.post("/reindex")
def reindex() -> Dict[str, str]:
    """
    Reindex all documents (data/raw/ and uploads/).
    This rebuilds the entire vector store.
    
    Returns:
        Status message
    """
    try:
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "tools" / "reindex.py")],
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(BASE_DIR)
        )
        
        if result.returncode == 0:
            return {
                "message": "Reindexing complete",
                "status": "success"
            }
        else:
            return {
                "message": f"Reindex failed: {result.stderr}",
                "status": "error"
            }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="Reindex timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reindex error: {str(e)}")


@router.get("/metrics")
def metrics() -> Dict:
    """
    Get all logged metrics and query history.
    
    Returns:
        Dict with 'queries' list and 'stats' summary
    """
    return {
        "queries": load_metrics().get("queries", []),
        "stats": get_stats()
    }


@router.get("/health")
def health() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Status message
    """
    return {"status": "ok", "message": "Knowledge Assistant backend running"}



@router.get("/source")
def get_source(file: str) -> FileResponse:
    """
    Serve a source file from `data/raw` or `uploads`.

    Args:
        file: Filename to serve (basename only)

    Returns:
        FileResponse for download or viewing
    """
    # Prevent path traversal
    safe_name = os.path.basename(file)

    candidate_folders = [
        BASE_DIR / "data" / "raw",
        UPLOADS_DIR,
    ]

    for folder in candidate_folders:
        for root, _, files in os.walk(folder):
            if safe_name in files:
                return FileResponse(os.path.join(root, safe_name), filename=safe_name)

    raise HTTPException(status_code=404, detail="Source file not found")


@router.get("/debug/search")
def debug_search(q: str):
    """
    Debug helper: return raw vector search results for a query.

    This is safe and read-only; it helps inspect top-k hits, distances, and
    short text snippets so you can confirm whether uploaded files were found
    and how similar they are.
    """
    try:
        from core.vector_store import search as _search
        docs = _search(q, k=5)
        results = []
        for d in docs:
            results.append({
                "id": d.get("id"),
                "source": d.get("source", "unknown"),
                "distance": d.get("distance"),
                "text_snippet": (d.get("text") or "")[:400]
            })
        return {"query": q, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debug search error: {e}")