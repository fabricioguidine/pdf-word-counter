"""Command-line interface for the PDF Word Counter."""
import argparse
import sys
from pathlib import Path

from src.application.use_cases.count_words_use_case import CountWordsUseCase
from src.application.use_cases.extract_words_use_case import ExtractWordsUseCase
from src.infrastructure.repositories.pdf_repository import PyPdfRepository
from src.infrastructure.services.nlp_service import SpacyNlpService
from src.infrastructure.services.output_service import ConsoleOutputService


def _force_utf8_stdout() -> None:
    """Force UTF-8 console output so PDF text with non-ASCII chars prints on any OS.

    On Windows the default console encoding is often cp1252, which raises
    UnicodeEncodeError when printing tokens extracted from a PDF.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Count words in a PDF file using NLP processing.",
    )
    parser.add_argument(
        "pdf_path",
        type=str,
        help="Path to the PDF file to analyze.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of top frequent words to display (default: 10).",
    )
    parser.add_argument(
        "--no-stopwords",
        action="store_true",
        help="Exclude stopwords from the analysis.",
    )
    return parser


def main() -> None:
    """Main entry point for the CLI."""
    _force_utf8_stdout()
    parser = create_parser()
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    repository = PyPdfRepository()
    nlp_service = SpacyNlpService()
    output_service = ConsoleOutputService()

    extract_use_case = ExtractWordsUseCase(repository, nlp_service)
    count_use_case = CountWordsUseCase(extract_use_case)

    statistics = count_use_case.execute(
        pdf_path,
        top_n=args.top,
        exclude_stopwords=args.no_stopwords,
    )
    output_service.display_statistics(statistics)
