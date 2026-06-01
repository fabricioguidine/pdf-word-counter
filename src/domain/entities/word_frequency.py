"""Word frequency entity: a word and how many times it occurred."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WordFrequency:
    """A word (as plain text) paired with its occurrence count."""

    word: str
    count: int

    def __lt__(self, other: "WordFrequency") -> bool:
        return self.count < other.count

    def __gt__(self, other: "WordFrequency") -> bool:
        return self.count > other.count
