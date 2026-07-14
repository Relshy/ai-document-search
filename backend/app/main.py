from fastapi import FastAPI, HTTPException, UploadFile

from app.chunking import chunk_text
from app.documents import UnsupportedDocumentType, extract_text

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

    return {"filename": file.filename or "", "chunks": chunk_text(text)}
