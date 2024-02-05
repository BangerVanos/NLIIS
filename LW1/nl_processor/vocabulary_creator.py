import spacy
from .configs import NLConfigManager


class LexemeCreator:

    def __init__(self, raw_text: str) -> None:
        self._raw_text = raw_text
        self._nlp = spacy.load(NLConfigManager.spacy_core())
    
    def get_lemmas(self) -> list[str]:
        spacy_text = self._nlp(self._raw_text)
        return [token.lemma_ for token in spacy_text]        
