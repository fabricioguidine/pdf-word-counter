"""Aggregated statistics from a word-frequency analysis."""

from dataclasses import dataclass

from .word_frequency import WordFrequency


@dataclass(frozen=True)
class WordStatistics:
    """Totals and the most frequent words for one analyzed document."""

    total_words: int
    unique_words: int
    total_pages: int
    top_words: list[WordFrequency]
