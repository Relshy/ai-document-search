from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_markdown_document_returns_extracted_text() -> None:
    files = {"file": ("notes.md", b"# Heading\n\nBody text.", "text/markdown")}

    with (
        patch("app.main.embed_chunks", return_value=[[0.1, 0.2, 0.3]]),
        patch("app.main.store_chunks") as mock_store_chunks,
    ):
        response = client.post("/documents", files=files)

    mock_store_chunks.assert_called_once_with(
        "notes.md", ["# Heading Body text."], [[0.1, 0.2, 0.3]]
    )

    assert response.status_code == 200
    assert response.json() == {
        "filename": "notes.md",
        "chunks": ["# Heading Body text."],
        "embedding_dimension": 3,
    }


def test_upload_blank_document_returns_zero_embedding_dimension() -> None:
    files = {"file": ("empty.md", b"   ", "text/markdown")}

    with (
        patch("app.main.embed_chunks", return_value=[]) as mock_embed_chunks,
        patch("app.main.store_chunks") as mock_store_chunks,
    ):
        response = client.post("/documents", files=files)

    mock_embed_chunks.assert_called_once_with([])
    mock_store_chunks.assert_called_once_with("empty.md", [], [])

    assert response.status_code == 200
    assert response.json() == {
        "filename": "empty.md",
        "chunks": [],
        "embedding_dimension": 0,
    }


def test_upload_unsupported_document_returns_error() -> None:
    files = {"file": ("archive.zip", b"binary data", "application/zip")}

    response = client.post("/documents", files=files)

    assert response.status_code == 422
    assert response.json()["detail"] == "Unsupported document type: .zip"
