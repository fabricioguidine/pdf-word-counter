"""NLP service implementation using spaCy."""

import spacy

from ...domain.entities.word import Word
from ...domain.services.nlp_service import INLPService


class SpacyNlpService(INLPService):
    """Tokenizes text into alphabetic words using a spaCy pipeline."""

    def __init__(self, model_name: str = "en_core_web_sm"):
        # Only the tokenizer + a stopword/lexeme lookup are needed; disabling
        # the heavy components keeps per-call cost low and behavior stable.
        self._nlp = spacy.load(model_name, disable=["parser", "ner", "tagger", "lemmatizer"])

    def extract_words(self, text: str) -> list[Word]:
        doc = self._nlp(text)
        words: list[Word] = []
        for token in doc:
            if token.is_alpha:
                words.append(Word(text=token.text, is_stopword=token.is_stop))
        return words
