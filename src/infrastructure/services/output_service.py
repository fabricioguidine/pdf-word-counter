"""Console output service: prints statistics to stdout."""

from ...domain.entities.word_statistics import WordStatistics
from ...domain.services.output_service import IOutputService


class ConsoleOutputService(IOutputService):
    """Renders word statistics as plain text on stdout."""

    def display_statistics(self, statistics: WordStatistics) -> None:
        print(f"Total pages: {statistics.total_pages}")
        print(f"Total words: {statistics.total_words}")
        print(f"Unique words: {statistics.unique_words}")
        print("Top words:")
        for wf in statistics.top_words:
            print(f"  {wf.word}: {wf.count}")
