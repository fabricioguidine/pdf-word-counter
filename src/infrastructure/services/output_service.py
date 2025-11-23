"""Output service implementation for file writing."""

from pathlib import Path
from typing import List

from ...domain.services.output_service import IOutputService


class FileOutputService(IOutputService):
    """Concrete implementation of output service for file writing."""

    def write(self, lines: List[str], output_path: str) -> None:
        """Write output lines to a file.

        Args:
            lines: List of strings to write.
            output_path: Path to the output file.
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


