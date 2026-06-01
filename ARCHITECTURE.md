# Architecture

PDF Word Counter is organized around Clean Architecture: dependencies point
inward, and the inner layers (domain, application) know nothing about the outer
layers (infrastructure, presentation).

## Layers and components

### Domain (`src/domain`)

Pure business logic with no third-party dependencies.

- `entities/word.py` — `Word`: a token with `text`, `is_stopword`, `lemma`.
- `entities/word_frequency.py` — `WordFrequency`: a word and its count.
- `entities/word_statistics.py` — `WordStatistics`: aggregate totals plus the
  ranked top words.
- `repositories/pdf_repository.py` — `PdfRepository`: abstract interface for
  reading PDF text and page counts.
- `services/nlp_service.py` — `NlpService`: abstract interface for turning raw
  text into `Word` entities.
- `services/output_service.py` — `OutputService`: abstract interface for
  presenting results.

### Application (`src/application`)

Use cases that orchestrate the domain via its abstract interfaces.

- `use_cases/extract_words_use_case.py` — `ExtractWordsUseCase`: reads text and
  page count from a `PdfRepository`, then tokenizes via an `NlpService`.
- `use_cases/count_words_use_case.py` — `CountWordsUseCase`: optionally filters
  stopwords, counts frequencies, and builds a `WordStatistics`.

### Infrastructure (`src/infrastructure`)

Concrete implementations of the domain interfaces.

- `repositories/pdf_repository.py` — `PyPdfRepository`: implements
  `PdfRepository` with `pypdf`.
- `services/nlp_service.py` — `SpacyNlpService`: implements `NlpService` with
  spaCy's `en_core_web_sm`, auto-downloading the model if it is missing.
- `services/output_service.py` — `ConsoleOutputService`: implements
  `OutputService` by printing to the console.

### Presentation (`src/presentation`)

- `cli.py` — argument parsing, dependency wiring, and the program entry point
  used by `main.py`.

## Data flow

```
main.py
  -> cli.main()
       parse args, validate path
       wire: PyPdfRepository, SpacyNlpService, ConsoleOutputService
       ExtractWordsUseCase(repo, nlp)
       CountWordsUseCase(extract)
         -> repo.extract_text(pdf)      # pypdf -> raw text
         -> repo.get_page_count(pdf)    # pypdf -> page count
         -> nlp.process_text(text)      # spaCy -> [Word]
         -> Counter / most_common       # -> WordStatistics
       ConsoleOutputService.display_statistics(stats)
```

The dependency direction is always inward: `presentation` and `infrastructure`
depend on `domain`; `domain` depends on nothing in the project.

## Cross-platform strategy

- **Paths**: every path is a `pathlib.Path`; no separators or absolute paths
  are hardcoded, so the same code runs on POSIX and Windows.
- **Console encoding**: `cli._force_utf8_stdout()` calls
  `sys.stdout.reconfigure(encoding="utf-8")` (guarded for streams without
  `reconfigure`) so Unicode tokens print on Windows consoles that default to a
  legacy code page.
- **PDF bytes**: `pypdf` opens files in binary mode internally; the application
  never decodes PDF bytes with a platform-dependent text encoding.
- **Tests**: fixtures are written into pytest's `tmp_path`, and the CLI is
  invoked through `sys.executable`, keeping tests hermetic and OS-agnostic.
- **CI**: a 3x3 matrix (`ubuntu-latest`, `macos-latest`, `windows-latest` x
  Python 3.11/3.12/3.13) runs lint and the full test suite on every push and
  pull request.
