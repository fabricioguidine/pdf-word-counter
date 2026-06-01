"""Concrete implementation of the PDF repository using pypdf."""
from pathlib import Path

from pypdf import PdfReader

from src.domain.repositories.pdf_repository import IPDFRepository


class PyPdfRepository(IPDFRepository):
    """PDF repository implementation using the pypdf library."""

    def extract_text(self, pdf_path: Path) -> str:
        """Extract raw text from a PDF file."""
        reader = PdfReader(str(pdf_path))
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n".join(text_parts)

    def get_page_count(self, pdf_path: Path) -> int:
        """Return the number of pages in the PDF."""
        reader = PdfReader(str(pdf_path))
        return len(reader.pages)
