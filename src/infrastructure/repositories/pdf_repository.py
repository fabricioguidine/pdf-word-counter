"""PDF repository implementation using PyPDF2."""

import os
from pathlib import Path
from typing import List

from PyPDF2 import PdfReader

from ...domain.repositories.pdf_repository import IPDFRepository


class PDFRepository(IPDFRepository):
    """Concrete implementation of PDF repository using PyPDF2."""

    def get_pdf_files(self, folder_path: str) -> List[str]:
        """Get list of PDF file paths from a folder.

        Args:
            folder_path: Path to the folder containing PDF files.

        Returns:
            List of PDF file paths.
        """
        folder = Path(folder_path)
        if not folder.exists():
            return []

        return [
            str(pdf_file)
            for pdf_file in folder.iterdir()
            if pdf_file.is_file() and pdf_file.suffix.lower() == ".pdf"
        ]

    def extract_text(self, pdf_path: str) -> str:
        """Extract text content from a PDF file.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text content.

        Raises:
            Exception: If PDF cannot be read or processed.
        """
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text


