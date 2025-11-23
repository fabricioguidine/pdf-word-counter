"""Output service interface for writing results."""

from abc import ABC, abstractmethod
from typing import List


class IOutputService(ABC):
    """Interface for output services."""

    @abstractmethod
    def write(self, lines: List[str], output_path: str) -> None:
        """Write output lines to a file.

        Args:
            lines: List of strings to write.
            output_path: Path to the output file.
        """
        pass


