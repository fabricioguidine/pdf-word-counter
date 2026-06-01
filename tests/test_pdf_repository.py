"""Tests for the concrete PDF repository (text + page extraction)."""
from pathlib import Path

import pytest

from src.infrastructure.repositories.pdf_repository import PyPdfRepository


@pytest.fixture
def repository() -> PyPdfRepository:
    return PyPdfRepository()


def test_repository_instantiation(repository: PyPdfRepository) -> None:
    """The repository can be instantiated."""
    assert repository is not None


def test_page_count(repository: PyPdfRepository, sample_pdf: Path) -> None:
    """Page count matches the number of pages written."""
    assert repository.get_page_count(sample_pdf) == 2


def test_extract_text_contains_words(
    repository: PyPdfRepository, sample_pdf: Path
) -> None:
    """Extracted text contains every word written into the PDF."""
    text = repository.extract_text(sample_pdf)
    for word in ("alpha", "beta", "gamma", "delta"):
        assert word in text


def test_empty_pages_yield_no_text(repository: PyPdfRepository, make_pdf) -> None:
    """A PDF whose pages have no drawn text extracts to an empty string."""
    pdf = make_pdf(["", ""], name="empty.pdf")
    assert repository.get_page_count(pdf) == 2
    assert repository.extract_text(pdf).strip() == ""
