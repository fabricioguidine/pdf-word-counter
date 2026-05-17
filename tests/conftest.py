"""Shared test fixtures for pdf-word-counter."""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"

SAMPLE_TEXT = (
    "Clean architecture promotes separation of concerns. "
    "Testing makes architecture robust. "
    "Words repeat: testing, testing, architecture."
)


def _build_pdf(target: Path, body: str) -> None:
    """Build a tiny PDF at *target* containing *body*.

    Uses reportlab if available, otherwise falls back to a hand-rolled
    minimal PDF so the test suite does not require a heavy dependency on
    every CI matrix entry.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        from reportlab.pdfgen import canvas  # type: ignore[import-not-found]

        c = canvas.Canvas(str(target))
        text_obj = c.beginText(72, 720)
        for line in body.splitlines() or [body]:
            text_obj.textLine(line)
        c.drawText(text_obj)
        c.showPage()
        c.save()
        return
    except ImportError:
        pass

    # Fallback: minimal PDF spec. Good enough for PyPDF2 to parse.
    escaped = body.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 12 Tf 72 720 Td ({escaped}) Tj ET".encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>"
        ),
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets: list[int] = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref_pos = len(out)
    out += b"xref\n0 " + str(len(objects) + 1).encode() + b"\n"
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (
        b"trailer\n<< /Size "
        + str(len(objects) + 1).encode()
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode()
        + b"\n%%EOF\n"
    )
    target.write_bytes(bytes(out))


def _build_empty_pdf(target: Path) -> None:
    """Build a valid PDF with one empty page."""
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        from reportlab.pdfgen import canvas  # type: ignore[import-not-found]

        c = canvas.Canvas(str(target))
        c.showPage()
        c.save()
        return
    except ImportError:
        pass

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << >> >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets: list[int] = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref_pos = len(out)
    out += b"xref\n0 " + str(len(objects) + 1).encode() + b"\n"
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (
        b"trailer\n<< /Size "
        + str(len(objects) + 1).encode()
        + b" /Root 1 0 R >>\nstartxref\n"
        + str(xref_pos).encode()
        + b"\n%%EOF\n"
    )
    target.write_bytes(bytes(out))


@pytest.fixture(scope="session")
def sample_text() -> str:
    """Known content used to build the sample PDF."""
    return SAMPLE_TEXT


@pytest.fixture(scope="session")
def sample_pdf(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A small PDF containing known text content."""
    pdf_path = tmp_path_factory.mktemp("pdfs") / "sample.pdf"
    _build_pdf(pdf_path, SAMPLE_TEXT)
    return pdf_path


@pytest.fixture(scope="session")
def empty_pdf(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A valid PDF with one empty page (no text content)."""
    pdf_path = tmp_path_factory.mktemp("pdfs") / "empty.pdf"
    _build_empty_pdf(pdf_path)
    return pdf_path


@pytest.fixture
def pdf_folder(tmp_path: Path, sample_pdf: Path, empty_pdf: Path) -> Path:
    """A folder containing one populated and one empty PDF."""
    folder = tmp_path / "pdfs"
    folder.mkdir()
    (folder / "sample.pdf").write_bytes(sample_pdf.read_bytes())
    (folder / "empty.pdf").write_bytes(empty_pdf.read_bytes())
    return folder
