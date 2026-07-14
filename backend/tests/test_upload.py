from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_markdown_document_returns_extracted_text() -> None:
    files = {"file": ("notes.md", b"# Heading\n\nBody text.", "text/markdown")}

    with patch("app.main.embed_chunks", return_value=[[0.1, 0.2, 0.3]]):
        response = client.post("/documents", files=files)

    assert response.status_code == 200
    assert response.json() == {
        "filename": "notes.md",
        "chunks": ["# Heading Body text."],
        "embedding_dimension": 3,
    }


def test_upload_unsupported_document_returns_error() -> None:
    files = {"file": ("archive.zip", b"binary data", "application/zip")}

    response = client.post("/documents", files=files)

    assert response.status_code == 422
    assert response.json()["detail"] == "Unsupported document type: .zip"
