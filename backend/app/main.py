from fastapi import FastAPI, HTTPException, UploadFile

from app.chunking import chunk_text
from app.documents import UnsupportedDocumentType, extract_text
from app.embedding import embed_chunks

app = FastAPI(title="ai-document-search")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/documents")
async def upload_document(file: UploadFile) -> dict[str, object]:
    content = await file.read()

    try:
        text = extract_text(file.filename or "", content)
    except UnsupportedDocumentType as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)

    return {
        "filename": file.filename or "",
        "chunks": chunks,
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
    }
