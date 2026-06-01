"""Output service interface for presenting statistics."""

from abc import ABC, abstractmethod

from ..entities.word_statistics import WordStatistics


class IOutputService(ABC):
    """Interface for rendering word statistics to the user."""

    @abstractmethod
    def display_statistics(self, statistics: WordStatistics) -> None:
        """Render the analysis results."""
        ...
