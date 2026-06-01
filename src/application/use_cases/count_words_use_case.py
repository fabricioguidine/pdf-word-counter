"""Use case for counting words in a PDF."""
from collections import Counter
from pathlib import Path

from src.application.use_cases.extract_words_use_case import ExtractWordsUseCase
from src.domain.entities.word_frequency import WordFrequency
from src.domain.entities.word_statistics import WordStatistics


class CountWordsUseCase:
    """Orchestrates the word counting process."""

    def __init__(self, extract_use_case: ExtractWordsUseCase) -> None:
        self._extract_use_case = extract_use_case

    def execute(
        self,
        pdf_path: Path,
        top_n: int = 10,
        exclude_stopwords: bool = False,
    ) -> WordStatistics:
        """Execute the word counting use case."""
        words, page_count = self._extract_use_case.execute(pdf_path)

        if exclude_stopwords:
            words = [w for w in words if not w.is_stopword]

        counter = Counter(w.text for w in words)
        top_words = counter.most_common(top_n)

        return WordStatistics(
            total_words=len(words),
            unique_words=len(counter),
            total_pages=page_count,
            top_words=[WordFrequency(word=w, count=c) for w, c in top_words],
        )
