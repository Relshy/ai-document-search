from io import BytesIO

from pypdf import PdfWriter

from app.documents import UnsupportedDocumentType, extract_text


def test_extract_text_from_markdown() -> None:
    content = b"# Title\n\nSome body text."

    text = extract_text("notes.md", content)

    assert text == "# Title\n\nSome body text."


def test_extract_text_from_pdf() -> None:
    content = _build_pdf_bytes()

    text = extract_text("scan.pdf", content)

    assert text == ""


def test_extract_text_rejects_unsupported_extension() -> None:
    try:
        extract_text("archive.zip", b"binary data")
        assert False, "expected UnsupportedDocumentType to be raised"
    except UnsupportedDocumentType as error:
        assert error.extension == ".zip"


def _build_pdf_bytes() -> bytes:
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()
