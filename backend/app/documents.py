from io import BytesIO

import pytesseract
from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".pdf", ".md"}


class UnsupportedDocumentType(Exception):
    def __init__(self, extension: str) -> None:
        self.extension = extension
        super().__init__(f"Unsupported document type: {extension}")


def extract_text(filename: str, content: bytes) -> str:
    extension = _extension_of(filename)

    if extension == ".md":
        return content.decode("utf-8")

    if extension == ".pdf":
        return _extract_pdf_text(content)

    raise UnsupportedDocumentType(extension)


def _extension_of(filename: str) -> str:
    if "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[1].lower()


def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    pages = [_extract_page_text(page) for page in reader.pages]
    return "\n".join(pages).strip()


def _extract_page_text(page) -> str:
    text = page.extract_text() or ""
    if text.strip():
        return text
    return _ocr_page_images(page)


def _ocr_page_images(page) -> str:
    scanned_text = [pytesseract.image_to_string(image.image) for image in page.images]
    return "\n".join(text.strip() for text in scanned_text if text.strip())
