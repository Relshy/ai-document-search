# ai-document-search

A small FastAPI backend for uploading documents and asking questions about them. Upload a PDF, a scanned image, or a Markdown file, and it gets chunked, embedded, and stored in Postgres with pgvector. From there you can run a semantic search over your documents, or ask a plain-language question and get an answer with citations back to the source chunks.

This is a backend only right now. There's no web frontend, just the API.

## How it works

Documents go through `POST /documents`. Text is pulled out with pypdf for PDFs and Tesseract OCR for scanned pages, split into chunks, embedded with sentence-transformers, and written to a pgvector column.

`GET /search?query=...` embeds your query and returns the closest chunks by vector similarity.

`GET /ask?query=...` does the same search, then sends the retrieved chunks to Claude along with your question and asks it to answer using only that context, citing which chunks it used.

## Running it

You need Docker and an Anthropic API key.

```
ANTHROPIC_API_KEY=sk-... docker compose up
```

This starts Postgres (with the pgvector extension) and the backend on port 8000.

To run it without Docker, install `backend/requirements.txt` into a virtualenv, point `DATABASE_URL` at a pgvector-enabled Postgres instance, and run `uvicorn app.main:app`.

## Tests

```
cd backend
pip install -r requirements.txt
pytest
```

34 tests, covering parsing, chunking, embedding, storage, search, and question answering, including the OCR fallback and edge cases like empty queries and zero-chunk uploads.

## What's not here

No auth, no rate limiting, no frontend. It's a working core, not a finished product. The four endpoints in `app/main.py` are the whole surface area, and each module (`documents.py`, `chunking.py`, `embedding.py`, `storage.py`, `qa.py`) does roughly what its name says.
