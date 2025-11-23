"""NLP service implementation using spaCy."""

from typing import List

import spacy

from ...domain.entities.word import Word
from ...domain.services.nlp_service import INLPService


class SpacyNLPService(INLPService):
    """Concrete implementation of NLP service using spaCy."""

    def __init__(self, model_name: str = "en_core_web_sm"):
        """Initialize the NLP service with a spaCy model.

        Args:
            model_name: Name of the spaCy model to load (default: "en_core_web_sm").
        """
        self._nlp = spacy.load(model_name)

    def extract_words(self, text: str) -> List[Word]:
        """Extract meaningful words from text.

        Args:
            text: Input text to process.

        Returns:
            List of extracted Word entities.
        """
        doc = self._nlp(text.lower())
        words: List[Word] = []

        # Extract single words (nouns, proper nouns, verbs)
        single_words = [
            Word(text=token.text, is_compound=False)
            for token in doc
            if token.pos_ in ("NOUN", "PROPN", "VERB") and len(token.text) > 2
        ]
        words.extend(single_words)

        # Extract compound terms (noun chunks with multiple words)
        compound_terms = [
            Word(text=chunk.text, is_compound=True)
            for chunk in doc.noun_chunks
            if len(chunk.text.split()) > 1
        ]
        words.extend(compound_terms)

        return words

