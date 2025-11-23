"""PDF repository interface."""

from abc import ABC, abstractmethod
from typing import List


class IPDFRepository(ABC):
    """Interface for PDF document repositories."""

    @abstractmethod
    def get_pdf_files(self, folder_path: str) -> List[str]:
        """Get list of PDF file paths from a folder.

        Args:
            folder_path: Path to the folder containing PDF files.

        Returns:
            List of PDF file paths.
        """
        pass

    @abstractmethod
    def extract_text(self, pdf_path: str) -> str:
        """Extract text content from a PDF file.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted text content.

        Raises:
            Exception: If PDF cannot be read or processed.
        """
        pass


