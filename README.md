# PDF Word Counter

A clean-architecture PDF word counter with NLP capabilities, built with Python.
Runs on Linux, macOS, and Windows.

## Features

- **PDF Text Extraction**: Extract text from PDF files using `pypdf`
- **NLP Processing**: Tokenization and linguistic analysis with `spaCy`
- **Word Frequency Analysis**: Count and rank words by frequency
- **Stopword Filtering**: Optionally exclude common stopwords
- **Clean Architecture**: Domain-driven design with clear separation of concerns
- **Cross-platform**: Verified on Linux, macOS, and Windows in CI

## Architecture

The project follows Clean Architecture principles:

```
src/
├── domain/              # Business logic and entities
│   ├── entities/        # Core data structures
│   ├── repositories/    # Abstract interfaces
│   └── services/        # Abstract service interfaces
├── application/         # Use cases
│   └── use_cases/       # Application-specific business rules
├── infrastructure/      # External implementations
│   ├── repositories/    # Concrete repository implementations
│   └── services/        # Concrete service implementations
└── presentation/        # User interface (CLI)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for components, data flow, and the
cross-platform strategy.

## Installation

Clone the repository:

```bash
git clone https://github.com/fabricioguidine/pdf-word-counter.git
cd pdf-word-counter
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

> The CLI also downloads `en_core_web_sm` automatically on first run if it is
> not already installed.

## Usage

```bash
python main.py path/to/document.pdf
```

### Options

- `--top N`: Display the top N most frequent words (default: 10)
- `--no-stopwords`: Exclude stopwords from the analysis

### Example

```bash
python main.py sample_pdfs/document.pdf --top 20 --no-stopwords
```

## Testing

Install the development dependencies (test tooling, `reportlab` for building
PDF fixtures, and the pinned spaCy model) and run the suite:

### Linux / macOS

```bash
pip install -r requirements-dev.txt
pytest -q
```

### Windows (PowerShell)

```powershell
pip install -r requirements-dev.txt
pytest -q
```

The end-to-end tests generate small PDF fixtures at test time with `reportlab`
into a temporary directory, run the real counter (both the public API and the
CLI as a subprocess), and assert the word, page, and frequency counts. They are
fully hermetic and do not depend on any committed binary file.

## Cross-platform notes

- All filesystem access uses `pathlib.Path`; there are no hardcoded path
  separators or absolute paths.
- The CLI forces UTF-8 console output (`sys.stdout.reconfigure`) so that text
  extracted from PDFs prints correctly on Windows consoles that default to
  legacy code pages.
- Tests use `tmp_path` and `sys.executable`, so they behave identically on
  Linux, macOS, and Windows.
- CI runs the matrix `ubuntu-latest`, `macos-latest`, `windows-latest` against
  Python 3.11, 3.12, and 3.13.

## License

MIT License - see [LICENSE](LICENSE) file for details.
