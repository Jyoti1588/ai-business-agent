from fastapi import APIRouter, UploadFile, File
import os

from backend.rag.ingest import ingest_document
from backend.rag.vectorstore.faiss_store import search as rag_search

router = APIRouter()

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = open(file_path, "r", errors="ignore").read()

    ingest_document(text)

    return {"status": "indexed", "file": file.filename}


@router.post("/ask-document")
def ask_document(request: dict):

    question = request.get("question", "")

    results = rag_search(question)

    return {
        "question": question,
        "context": results
    }