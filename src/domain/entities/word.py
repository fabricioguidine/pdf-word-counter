"""Word entity representing a single token extracted from a document."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Word:
    """A single word token, normalized to lowercase."""

    text: str
    is_stopword: bool = False

    def __post_init__(self):
        object.__setattr__(self, "text", self.text.lower().strip())

    def __len__(self) -> int:
        return len(self.text)
