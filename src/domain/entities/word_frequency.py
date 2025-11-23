"""Word frequency entity representing word count and weight."""

from dataclasses import dataclass
from typing import Optional

from .word import Word


@dataclass(frozen=True)
class WordFrequency:
    """Represents a word with its frequency count and relative weight."""

    word: Word
    count: int
    weight: float

    @classmethod
    def create(cls, word: Word, count: int, max_frequency: int) -> "WordFrequency":
        """Create a WordFrequency with calculated weight."""
        weight = round(count / max_frequency, 4) if max_frequency > 0 else 0.0
        return cls(word=word, count=count, weight=weight)

    def __lt__(self, other: "WordFrequency") -> bool:
        """Compare by count for sorting."""
        return self.count < other.count

    def __gt__(self, other: "WordFrequency") -> bool:
        """Compare by count for sorting."""
        return self.count > other.count


