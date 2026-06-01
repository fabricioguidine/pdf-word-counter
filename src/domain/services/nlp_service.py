"""NLP service interface for tokenizing text into words."""

from abc import ABC, abstractmethod

from ..entities.word import Word


class INLPService(ABC):
    """Interface for Natural Language Processing services."""

    @abstractmethod
    def extract_words(self, text: str) -> list[Word]:
        """Tokenize text into a list of Word entities (in order)."""
        ...
