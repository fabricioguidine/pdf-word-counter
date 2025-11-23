"""Word statistics entity representing aggregated word analysis results."""

from dataclasses import dataclass
from typing import List

from .word_frequency import WordFrequency


@dataclass(frozen=True)
class WordStatistics:
    """Represents aggregated statistics from word frequency analysis."""

    total_unique_words: int
    total_words: int
    top_words: List[WordFrequency]
    max_frequency: int

    @property
    def top_percentage(self) -> float:
        """Calculate the percentage of top words relative to unique words."""
        if self.total_unique_words == 0:
            return 0.0
        return len(self.top_words) / self.total_unique_words * 100


