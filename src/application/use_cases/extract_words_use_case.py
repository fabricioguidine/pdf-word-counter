"""Use case for extracting words from PDF files."""

from typing import List, Tuple

from ...domain.entities.word import Word
from ...domain.repositories.pdf_repository import IPDFRepository
from ...domain.services.nlp_service import INLPService


class ExtractWordsUseCase:
    """Use case for extracting words from PDF documents."""

    def __init__(
        self,
        pdf_repository: IPDFRepository,
        nlp_service: INLPService,
    ):
        """Initialize the use case with required dependencies.

        Args:
            pdf_repository: Repository for accessing PDF files.
            nlp_service: Service for NLP processing.
        """
        self._pdf_repository = pdf_repository
        self._nlp_service = nlp_service

    def execute(self, folder_path: str) -> Tuple[List[Word], List[str]]:
        """Extract words from all PDF files in a folder.

        Args:
            folder_path: Path to folder containing PDF files.

        Returns:
            Tuple of (extracted words, error messages).
        """
        all_words: List[Word] = []
        errors: List[str] = []

        pdf_files = self._pdf_repository.get_pdf_files(folder_path)

        for pdf_path in pdf_files:
            try:
                text = self._pdf_repository.extract_text(pdf_path)
                words = self._nlp_service.extract_words(text)
                all_words.extend(words)
            except Exception as e:
                errors.append(f"❌ Erro ao ler {pdf_path}: {e}")

        return all_words, errors


