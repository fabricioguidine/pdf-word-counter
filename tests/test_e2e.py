"""End-to-end tests driving the real word counter from PDF to result.

These tests run the full pipeline: a generated PDF -> pypdf extraction ->
spaCy tokenization -> frequency counting. They also drive the CLI in a
subprocess using ``sys.executable`` so the behaviour is OS-agnostic.
"""
import subprocess
import sys
from pathlib import Path

import pytest

from src.application.use_cases.count_words_use_case import CountWordsUseCase
from src.application.use_cases.extract_words_use_case import ExtractWordsUseCase
from src.infrastructure.repositories.pdf_repository import PyPdfRepository
from src.infrastructure.services.nlp_service import SpacyNlpService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def nlp_service() -> SpacyNlpService:
    """A single spaCy service shared across tests (model load is expensive)."""
    return SpacyNlpService()


def _count(nlp_service, pdf_path, **kwargs):
    repo = PyPdfRepository()
    extract = ExtractWordsUseCase(repo, nlp_service)
    return CountWordsUseCase(extract).execute(pdf_path, **kwargs)


def test_end_to_end_counts(nlp_service, sample_pdf: Path) -> None:
    """The full pipeline reports the expected totals and frequencies."""
    stats = _count(nlp_service, sample_pdf, top_n=10)

    assert stats.total_pages == 2
    assert stats.total_words == 8
    assert stats.unique_words == 4

    counts = {wf.word: wf.count for wf in stats.top_words}
    assert counts == {"alpha": 1, "beta": 2, "gamma": 3, "delta": 2}
    # Most frequent word ranks first.
    assert stats.top_words[0].word == "gamma"


def test_top_n_limits_results(nlp_service, sample_pdf: Path) -> None:
    """top_n caps the number of returned frequencies without changing totals."""
    stats = _count(nlp_service, sample_pdf, top_n=2)
    assert len(stats.top_words) == 2
    assert stats.total_words == 8


def test_multi_page_aggregation(nlp_service, make_pdf) -> None:
    """Words are aggregated across many pages (edge case: 5 pages)."""
    pages = ["river river"] * 5
    pdf = make_pdf(pages, name="multi.pdf")
    stats = _count(nlp_service, pdf, top_n=5)

    assert stats.total_pages == 5
    assert stats.total_words == 10
    assert stats.unique_words == 1
    assert stats.top_words[0].word == "river"
    assert stats.top_words[0].count == 10


def test_empty_pages_produce_zero_words(nlp_service, make_pdf) -> None:
    """Edge case: a PDF with empty pages yields no words but counts pages."""
    pdf = make_pdf(["", ""], name="blank.pdf")
    stats = _count(nlp_service, pdf, top_n=10)

    assert stats.total_pages == 2
    assert stats.total_words == 0
    assert stats.unique_words == 0
    assert stats.top_words == []


def test_exclude_stopwords(nlp_service, make_pdf) -> None:
    """The --no-stopwords path drops common stopwords from the totals."""
    pdf = make_pdf(["the the cat the dog"], name="stop.pdf")

    with_stop = _count(nlp_service, pdf, exclude_stopwords=False)
    without_stop = _count(nlp_service, pdf, exclude_stopwords=True)

    assert with_stop.total_words == 5
    assert without_stop.total_words < with_stop.total_words
    words_kept = {wf.word for wf in without_stop.top_words}
    assert "the" not in words_kept
    assert {"cat", "dog"} <= words_kept


def test_cli_end_to_end(sample_pdf: Path) -> None:
    """The CLI runs as a subprocess and prints the statistics."""
    result = subprocess.run(
        [sys.executable, "main.py", str(sample_pdf), "--top", "5"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, result.stderr
    assert "Total words: 8" in result.stdout
    assert "Total pages: 2" in result.stdout
    assert "gamma: 3" in result.stdout


def test_cli_missing_file_exits_nonzero(tmp_path: Path) -> None:
    """The CLI exits non-zero with a clear error for a missing file."""
    missing = tmp_path / "does-not-exist.pdf"
    result = subprocess.run(
        [sys.executable, "main.py", str(missing)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 1
    assert "File not found" in result.stderr
