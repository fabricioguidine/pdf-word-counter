"""Command-line interface for the PDF word counter application."""

import os
from pathlib import Path

from ..application.use_cases.count_words_use_case import CountWordsUseCase
from ..application.use_cases.extract_words_use_case import ExtractWordsUseCase
from ..infrastructure.repositories.pdf_repository import PDFRepository
from ..infrastructure.services.nlp_service import SpacyNLPService
from ..infrastructure.services.output_service import FileOutputService


class PDFWordCounterCLI:
    """Command-line interface for PDF word counting."""

    def __init__(
        self,
        pdf_folder: str = "sample_pdfs",
        output_file: str = "output.txt",
        nlp_model: str = "en_core_web_sm",
        top_percentage: float = 0.10,
    ):
        """Initialize the CLI with configuration.

        Args:
            pdf_folder: Path to folder containing PDF files.
            output_file: Path to output file for results.
            nlp_model: spaCy model name to use.
            top_percentage: Percentage of top words to include (default: 0.10 = 10%).
        """
        self._pdf_folder = pdf_folder
        self._output_file = output_file
        self._top_percentage = top_percentage

        # Initialize dependencies
        self._pdf_repository = PDFRepository()
        self._nlp_service = SpacyNLPService(model_name=nlp_model)
        self._output_service = FileOutputService()

        # Initialize use cases
        self._extract_words_use_case = ExtractWordsUseCase(
            pdf_repository=self._pdf_repository,
            nlp_service=self._nlp_service,
        )
        self._count_words_use_case = CountWordsUseCase(
            top_percentage=self._top_percentage
        )

    def run(self) -> None:
        """Execute the word counting process."""
        output_lines: list[str] = []

        # Get PDF files info
        pdf_files = self._pdf_repository.get_pdf_files(self._pdf_folder)
        if not pdf_files:
            output_lines.append("⚠️ Nenhum arquivo PDF encontrado na pasta.")
            self._output_service.write(output_lines, self._output_file)
            return

        # Extract words from PDFs
        words, errors = self._extract_words_use_case.execute(self._pdf_folder)

        # Add file processing info (count words per file)
        file_word_counts: dict[str, int] = {}
        for pdf_path in pdf_files:
            try:
                text = self._pdf_repository.extract_text(pdf_path)
                file_words = self._nlp_service.extract_words(text)
                file_name = Path(pdf_path).name
                file_word_counts[file_name] = len(file_words)
            except Exception:
                pass  # Error already handled in use case

        for file_name, count in file_word_counts.items():
            output_lines.append(f"{file_name}: {count} palavras úteis")

        # Add errors if any
        output_lines.extend(errors)

        # Count words and generate statistics
        statistics = self._count_words_use_case.execute(words)

        if statistics.total_unique_words == 0:
            output_lines.append("⚠️ Nenhuma palavra útil encontrada nos PDFs.")
            self._output_service.write(output_lines, self._output_file)
            return

        # Format output
        output_lines.append(f"\n🔢 Palavras únicas úteis: {statistics.total_unique_words}")
        output_lines.append(
            f"\n🏆 Top {len(statistics.top_words)} palavras mais frequentes (com pesos):\n"
        )

        for i, word_freq in enumerate(statistics.top_words, start=1):
            line = (
                f"{i:02d}. {word_freq.word.text:<25} → "
                f"{word_freq.count:>4}x | peso: {word_freq.weight:.2f}"
            )
            output_lines.append(line)

        # Write output
        self._output_service.write(output_lines, self._output_file)


def main():
    """Main entry point for the CLI application."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    pdf_folder = project_root / "sample_pdfs"
    output_file = project_root / "output.txt"

    cli = PDFWordCounterCLI(
        pdf_folder=str(pdf_folder),
        output_file=str(output_file),
    )
    cli.run()


if __name__ == "__main__":
    main()

