import spacy
import lemminflect as lm
from .configs import NLConfigManager
from dataclasses import dataclass


@dataclass(frozen=True)
class VocabularyUnit:
    lemma: str
    pos: str    


class VocabularyCreator:

    def __init__(self, raw_text: str) -> None:
        self._raw_text = raw_text
        self._nlp = spacy.load(NLConfigManager.spacy_core())
        self._vocabulary_units: list[VocabularyUnit] | None = None
    
    def get_vocabulary_units(self) -> list[VocabularyUnit]:
        spacy_text = self._nlp(self._raw_text)
        self._vocabulary_units = sorted(set([VocabularyUnit(token.lemma_, token.pos_) for token in spacy_text
                                             if token.is_alpha and token.is_ascii]),
                                            key=lambda unit: unit.lemma)
        return self._vocabulary_units  

    @staticmethod
    def get_inflections(lemma_list: list[str] | list[VocabularyUnit]):
        return {lemma: lm.getAllInflections(lemma.lemma if isinstance(lemma, VocabularyUnit) else lemma)
                for lemma in lemma_list} 

    @staticmethod
    def get_inflection(lemma: str | VocabularyUnit, tag: str) -> str | None:
        inflections = lm.getInflection(lemma.lemma if isinstance(lemma, VocabularyUnit) else lemma, tag)
        return inflections[0] if len(inflections) > 0 else None     
