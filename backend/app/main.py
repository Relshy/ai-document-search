from fastapi import FastAPI, HTTPException, UploadFile

from app.chunking import chunk_text
from app.documents import UnsupportedDocumentType, extract_text
from app.embedding import embed_chunks, embed_query
from app.qa import answer_question
from app.storage import search_chunks, store_chunks

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
    store_chunks(file.filename or "", chunks, embeddings)

    return {
        "filename": file.filename or "",
        "chunks": chunks,
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
    }


@app.get("/search")
def search_documents(query: str, limit: int = 5) -> dict[str, object]:
    if not query.strip():
        raise HTTPException(status_code=422, detail="query must not be empty")

    query_embedding = embed_query(query)
    results = search_chunks(query_embedding, limit=limit)

    return {"query": query, "results": results}


@app.get("/ask")
def ask_question(query: str, limit: int = 5) -> dict[str, object]:
    if not query.strip():
        raise HTTPException(status_code=422, detail="query must not be empty")

    result = answer_question(query, limit=limit)

    return {"query": query, "answer": result["answer"], "citations": result["citations"]}
