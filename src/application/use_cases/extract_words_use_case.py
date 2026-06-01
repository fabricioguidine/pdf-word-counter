"""Use case: extract the ordered word list and page count from one PDF."""

from pathlib import Path

from ...domain.entities.word import Word
from ...domain.repositories.pdf_repository import IPDFRepository
from ...domain.services.nlp_service import INLPService


class ExtractWordsUseCase:
    """Extracts words from a single PDF document."""

    def __init__(self, pdf_repository: IPDFRepository, nlp_service: INLPService):
        self._pdf_repository = pdf_repository
        self._nlp_service = nlp_service

    def execute(self, pdf_path: Path) -> tuple[list[Word], int]:
        text = self._pdf_repository.extract_text(pdf_path)
        page_count = self._pdf_repository.get_page_count(pdf_path)
        words = self._nlp_service.extract_words(text)
        return words, page_count
