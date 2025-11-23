"""Word entity representing a single word or compound term."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Word:
    """Represents a word or compound term extracted from text."""

    text: str
    is_compound: bool = False

    def __post_init__(self):
        """Normalize word text to lowercase."""
        object.__setattr__(self, "text", self.text.lower().strip())

    def __len__(self) -> int:
        """Return the length of the word text."""
        return len(self.text)


