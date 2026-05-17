"""Tests for the concrete PDF repository implementation."""

from __future__ import annotations

import re
from pathlib import Path

from src.infrastructure.repositories.pdf_repository import PDFRepository


def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z]+", text))


def test_extract_text_from_known_pdf_returns_expected_words(sample_pdf: Path) -> None:
    """Extraction must surface the known content of the sample PDF."""
    repo = PDFRepository()

    text = repo.extract_text(str(sample_pdf))

    assert isinstance(text, str)
    lowered = text.lower()
    # Words known to be embedded in the fixture
    for needle in ("architecture", "testing", "words"):
        assert needle in lowered, f"missing {needle!r} in extracted text: {text!r}"
    # Sanity check that we got a reasonable amount of words.
    assert _word_count(text) >= 10


def test_extract_text_from_empty_pdf_returns_empty_string(empty_pdf: Path) -> None:
    """A valid PDF that has no text content must yield an empty string."""
    repo = PDFRepository()

    text = repo.extract_text(str(empty_pdf))

    assert text == ""


def test_get_pdf_files_lists_only_pdfs(pdf_folder: Path) -> None:
    """Repository must only return *.pdf files from the folder."""
    (pdf_folder / "notes.txt").write_text("ignore me", encoding="utf-8")
    repo = PDFRepository()

    pdfs = repo.get_pdf_files(str(pdf_folder))

    names = sorted(Path(p).name for p in pdfs)
    assert names == ["empty.pdf", "sample.pdf"]


def test_get_pdf_files_missing_folder_returns_empty(tmp_path: Path) -> None:
    """A non-existent folder must return an empty list, not raise."""
    repo = PDFRepository()

    assert repo.get_pdf_files(str(tmp_path / "does-not-exist")) == []
