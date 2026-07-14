# ai-document-search

Semantic search and question answering over your own documents.

A self-hosted service that ingests documents, embeds them for semantic retrieval, and answers questions with cited sources.

## Status

Seed project. The goal, scope, and task list are defined here; the implementation is built incrementally. Work the tasks in the order of the build phases in CLAUDE.md.

## Ingestion

- [x] Upload PDFs and Markdown documents
- [x] OCR scanned documents
- [x] Chunk and embed documents

## Search

- [x] Semantic retrieval over documents
- [x] Question answering with cited sources
- [x] Highlight citations in results

## Tech stack

- Backend: Python + FastAPI
- Vector store: PostgreSQL with pgvector
- Embeddings: sentence-transformers
- OCR: Tesseract
- Question answering: Claude API
- Frontend: React + TypeScript
- Deployment: Docker Compose
