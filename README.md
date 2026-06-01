# pdf-word-counter

A CLI utility that counts word frequencies across PDF files using spaCy NLP. It reads every PDF in a folder, extracts meaningful terms, ranks the most frequent ones, and writes the result to a text file.

[![CI](https://github.com/fabricioguidine/pdf-word-counter/actions/workflows/ci.yml/badge.svg)](https://github.com/fabricioguidine/pdf-word-counter/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)

## Features

- **PDF text extraction** — reads every `.pdf` in the input folder and extracts text per page with PyPDF2.
- **NLP filtering** — keeps only nouns, proper nouns, and verbs longer than two characters via spaCy.
- **Compound terms** — detects multi-word noun chunks (e.g. "software testing") from spaCy noun chunks.
- **Frequency ranking** — counts term frequency across all PDFs and assigns each term a weight relative to the most frequent one.
- **Top cutoff** — reports the top 10% most frequent terms (at least one), ranked with count and weight.
- **File output** — writes per-file useful-word counts and the ranking to `output.txt`.

## Requirements

- Python 3.10 or newer.
- `PyPDF2==3.0.1` and `spacy==3.8.5` (see `requirements.txt`).
- A spaCy language model: `en_core_web_sm` (default) or `pt_core_news_sm` for Portuguese.

## Installation

```powershell
git clone https://github.com/fabricioguidine/pdf-word-counter.git
cd pdf-word-counter

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

For Portuguese text, download the Portuguese model instead:

```powershell
python -m spacy download pt_core_news_sm
```

## Usage

The tool takes no command-line arguments. Place the PDFs you want to analyze in `sample_pdfs/`, then run:

```powershell
python main.py
```

Equivalently, run the CLI module directly:

```powershell
python -m src.presentation.cli
```

Results are written to `output.txt` in the project root. The input folder, output file, spaCy model, and top-percentage cutoff are set in `PDFWordCounterCLI` (defaults: `sample_pdfs`, `output.txt`, `en_core_web_sm`, `0.10`).

The generated `output.txt` lists each PDF's useful-word count, the total number of unique useful words, and the weighted ranking:

```
file1.pdf: 1234 palavras úteis
file2.pdf: 567 palavras úteis

🔢 Palavras únicas úteis: 890

🏆 Top 89 palavras mais frequentes (com pesos):

01. software testing        →   45x | peso: 1.00
02. quality assurance       →   32x | peso: 0.71
03. test case               →   28x | peso: 0.62
```

## Project structure

```
pdf-word-counter/
├── main.py                     # Entry point -> src.presentation.cli.main
├── src/
│   ├── domain/                 # Entities, repository and service interfaces
│   │   ├── entities/           # Word, WordFrequency, WordStatistics
│   │   ├── repositories/       # IPDFRepository
│   │   └── services/           # INLPService, IOutputService
│   ├── application/
│   │   └── use_cases/          # ExtractWordsUseCase, CountWordsUseCase
│   ├── infrastructure/
│   │   ├── repositories/       # PDFRepository (PyPDF2)
│   │   └── services/           # SpacyNLPService, FileOutputService
│   └── presentation/
│       └── cli.py              # PDFWordCounterCLI
├── tests/                      # pytest suite
├── sample_pdfs/                # Input PDF files
├── requirements.txt
└── pyproject.toml
```

## Testing

```powershell
pip install -e ".[dev]"
pytest
```

Tests run with coverage configured in `pyproject.toml`.

## License

Released under the [MIT License](LICENSE).
