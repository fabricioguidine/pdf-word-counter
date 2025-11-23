"""NLP service interface for text processing."""

from abc import ABC, abstractmethod
from typing import List

from ..entities.word import Word


class INLPService(ABC):
    """Interface for Natural Language Processing services."""

    @abstractmethod
    def extract_words(self, text: str) -> List[Word]:
        """Extract meaningful words from text.

        Args:
            text: Input text to process.

        Returns:
            List of extracted Word entities.
        """
        pass

