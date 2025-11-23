"""Use case for counting word frequencies and calculating statistics."""

from collections import Counter
from typing import List

from ...domain.entities.word import Word
from ...domain.entities.word_frequency import WordFrequency
from ...domain.entities.word_statistics import WordStatistics


class CountWordsUseCase:
    """Use case for counting word frequencies and generating statistics."""

    def __init__(self, top_percentage: float = 0.10):
        """Initialize the use case.

        Args:
            top_percentage: Percentage of top words to include in results (default: 0.10 = 10%).
        """
        self._top_percentage = top_percentage

    def execute(self, words: List[Word]) -> WordStatistics:
        """Count word frequencies and generate statistics.

        Args:
            words: List of words to analyze.

        Returns:
            WordStatistics containing aggregated results.
        """
        if not words:
            return WordStatistics(
                total_unique_words=0,
                total_words=0,
                top_words=[],
                max_frequency=0,
            )

        word_counts = Counter(word.text for word in words)
        total_unique = len(word_counts)
        max_freq = word_counts.most_common(1)[0][1] if word_counts else 0

        weighted_frequencies = [
            WordFrequency.create(
                word=Word(text=word_text),
                count=count,
                max_frequency=max_freq,
            )
            for word_text, count in word_counts.items()
        ]

        weighted_frequencies.sort(key=lambda x: x.count, reverse=True)

        top_n = max(1, int(total_unique * self._top_percentage))
        top_words = weighted_frequencies[:top_n]

        return WordStatistics(
            total_unique_words=total_unique,
            total_words=len(words),
            top_words=top_words,
            max_frequency=max_freq,
        )


