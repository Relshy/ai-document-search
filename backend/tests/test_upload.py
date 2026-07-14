from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_markdown_document_returns_extracted_text() -> None:
    files = {"file": ("notes.md", b"# Heading\n\nBody text.", "text/markdown")}

    response = client.post("/documents", files=files)

    assert response.status_code == 200
    assert response.json() == {"filename": "notes.md", "text": "# Heading\n\nBody text."}


def test_upload_unsupported_document_returns_error() -> None:
    files = {"file": ("archive.zip", b"binary data", "application/zip")}

    response = client.post("/documents", files=files)

    assert response.status_code == 422
    assert response.json()["detail"] == "Unsupported document type: .zip"
