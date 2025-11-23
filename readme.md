# PDF Word Counter with Frequency Weighting

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/Architecture-Clean-blue.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

A Python application that processes PDF files, extracts meaningful words and compound terms using NLP analysis, calculates word frequencies, and generates weighted statistics. Built with **Clean Architecture** principles for maintainability and testability.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **PDF Text Extraction**: Extracts text from multiple PDF files in a folder
- **NLP-Based Word Extraction**: Uses spaCy for intelligent word extraction (nouns, proper nouns, verbs)
- **Compound Term Detection**: Identifies multi-word phrases (e.g., "software testing")
- **Frequency Analysis**: Counts word occurrences across all processed PDFs
- **Weighted Statistics**: Calculates relative weights based on maximum frequency
- **Top Words Report**: Generates a report with the top 10% most frequent words
- **Silent Mode**: Writes results to `output.txt` without terminal output
- **Clean Architecture**: Organized in layers (Domain, Application, Infrastructure, Presentation)

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

```
src/
├── domain/           # Business logic and entities
│   ├── entities/     # Domain models (Word, WordFrequency, WordStatistics)
│   ├── repositories/ # Repository interfaces
│   └── services/     # Service interfaces
├── application/      # Use cases and business rules
│   └── use_cases/    # Application-specific business logic
├── infrastructure/   # External dependencies and implementations
│   ├── repositories/ # Concrete repository implementations
│   └── services/     # Concrete service implementations
└── presentation/     # User interface layer
    └── cli.py        # Command-line interface
```

### Architecture Layers

- **Domain Layer**: Contains business entities and interfaces. No external dependencies.
- **Application Layer**: Implements use cases that orchestrate domain objects.
- **Infrastructure Layer**: Provides concrete implementations (PyPDF2, spaCy, file I/O).
- **Presentation Layer**: Handles user interaction (CLI).

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/fabricioguidine/pdf-word-counter.git
cd pdf-word-counter
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy language model

**For English texts:**
```bash
python -m spacy download en_core_web_sm
```

**For Portuguese texts:**
```bash
python -m spacy download pt_core_news_sm
```

## 💻 Usage

### Basic Usage

1. **Place your PDF files** in the `sample_pdfs/` folder

2. **Run the application:**
```bash
python main.py
```

Or directly:
```bash
python -m src.presentation.cli
```

3. **Check the results** in `output.txt`

### Output Format

The `output.txt` file contains:
- Processing status for each PDF file
- Total count of unique useful words
- Top 10% most frequent words with:
  - Word/term text
  - Frequency count
  - Relative weight (normalized to max frequency)

Example output:
```
file1.pdf: 1234 palavras úteis
file2.pdf: 567 palavras úteis

🔢 Palavras únicas úteis: 890

🏆 Top 89 palavras mais frequentes (com pesos):

01. software testing        →   45x | peso: 1.00
02. quality assurance       →   32x | peso: 0.71
03. test case               →   28x | peso: 0.62
...
```

## 📂 Project Structure

```
pdf-word-counter/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── word.py
│   │   │   ├── word_frequency.py
│   │   │   └── word_statistics.py
│   │   ├── repositories/
│   │   │   └── pdf_repository.py
│   │   └── services/
│   │       ├── nlp_service.py
│   │       └── output_service.py
│   ├── application/
│   │   └── use_cases/
│   │       ├── extract_words_use_case.py
│   │       └── count_words_use_case.py
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   └── pdf_repository.py
│   │   └── services/
│   │       ├── nlp_service.py
│   │       └── output_service.py
│   └── presentation/
│       └── cli.py
├── sample_pdfs/            # Input PDF files folder
├── output.txt              # Generated output file
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── LICENSE                 # License file
```

## 🛠️ Technologies

- **[PyPDF2](https://pypi.org/project/PyPDF2/)** - PDF text extraction
- **[spaCy](https://spacy.io/)** - Natural Language Processing
  - `en_core_web_sm` - English language model
  - `pt_core_news_sm` - Portuguese language model
- **Python 3.8+** - Programming language

## 🧪 Development

### Running Tests

```bash
# Add tests here when implemented
pytest tests/
```

### Code Style

This project follows PEP 8 style guidelines. Consider using:
- `black` for code formatting
- `flake8` or `pylint` for linting
- `mypy` for type checking

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Fabricio Guidine - [@fabricioguidine](https://github.com/fabricioguidine)

## 🙏 Acknowledgments

- spaCy team for the excellent NLP library
- PyPDF2 contributors for PDF processing capabilities

---

**Note**: This project uses Clean Architecture principles to ensure maintainability, testability, and separation of concerns. The architecture allows for easy extension and modification of individual components without affecting others.
