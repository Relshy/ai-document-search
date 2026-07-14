from io import BytesIO

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
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()
