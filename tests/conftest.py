"""Shared pytest fixtures.

Builds small, deterministic PDF fixtures at test time with reportlab so the
end-to-end tests are hermetic and do not depend on any committed binary file.
"""
import sys
from pathlib import Path

import pytest

# Ensure the project root is on sys.path for `src` imports regardless of OS.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

reportlab = pytest.importorskip("reportlab")


def _write_pdf(path: Path, pages: list[str]) -> Path:
    """Write a PDF with one drawn text line per page entry."""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    pdf = canvas.Canvas(str(path), pagesize=letter)
    for line in pages:
        if line:
            pdf.drawString(72, 720, line)
        pdf.showPage()
    pdf.save()
    return path


@pytest.fixture
def make_pdf(tmp_path: Path):
    """Return a factory that writes a PDF into the test's tmp_path."""

    def _factory(pages: list[str], name: str = "sample.pdf") -> Path:
        return _write_pdf(tmp_path / name, pages)

    return _factory


@pytest.fixture
def sample_pdf(make_pdf) -> Path:
    """A two-page PDF with known, deterministic word frequencies.

    Page 1: alpha beta beta gamma gamma gamma  (6 tokens)
    Page 2: delta delta                        (2 tokens)
    Total alphabetic tokens: 8, unique: 4 (alpha, beta, gamma, delta).
    """
    return make_pdf(
        [
            "alpha beta beta gamma gamma gamma",
            "delta delta",
        ]
    )
