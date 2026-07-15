from io import BytesIO

from PIL import Image
from pypdf import PdfWriter
from reportlab.pdfgen import canvas

from app import documents
from app.documents import UnsupportedDocumentType, extract_text


def test_extract_text_from_markdown() -> None:
    content = b"# Title\n\nSome body text."

    text = extract_text("notes.md", content)

    assert text == "# Title\n\nSome body text."


def test_extract_text_from_pdf() -> None:
    content = _build_pdf_bytes()

    text = extract_text("scan.pdf", content)

    assert text == ""


def test_extract_text_ocrs_scanned_pdf_pages(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        documents.pytesseract, "image_to_string", lambda image: "Scanned page text"
    )
    content = _build_scanned_pdf_bytes(tmp_path)

    text = extract_text("scan.pdf", content)

    assert text == "Scanned page text"


def test_extract_text_rejects_unsupported_extension() -> None:
    try:
        extract_text("archive.zip", b"binary data")
        assert False, "expected UnsupportedDocumentType to be raised"
    except UnsupportedDocumentType as error:
        assert error.extension == ".zip"


def test_extract_text_rejects_filename_without_extension() -> None:
    try:
        extract_text("archive", b"binary data")
        assert False, "expected UnsupportedDocumentType to be raised"
    except UnsupportedDocumentType as error:
        assert error.extension == ""


def _build_pdf_bytes() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def _build_scanned_pdf_bytes(tmp_path) -> bytes:
    image_path = tmp_path / "page.png"
    Image.new("RGB", (100, 50), color="white").save(image_path)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=(200, 200))
    pdf.drawImage(str(image_path), 10, 10, width=100, height=50)
    pdf.save()
    return buffer.getvalue()
