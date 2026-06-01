"""PDF repository interface."""

from abc import ABC, abstractmethod
from pathlib import Path


class IPDFRepository(ABC):
    """Interface for reading PDF documents."""

    @abstractmethod
    def extract_text(self, pdf_path: Path) -> str:
        """Extract the full text content of a PDF file."""
        ...

    @abstractmethod
    def get_page_count(self, pdf_path: Path) -> int:
        """Return the number of pages in a PDF file."""
        ...
