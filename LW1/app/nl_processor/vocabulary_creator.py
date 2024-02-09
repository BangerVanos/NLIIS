import spacy
import lemminflect as lm
from .configs import NLConfigManager
from dataclasses import dataclass
import os
import json


@dataclass(frozen=True)
class VocabularyUnit:
    lemma: str
    pos: str    


class VocabularyCreator:
    """Class that creates vocabulary according to task"""

    def __init__(self, raw_text: str) -> None:
        self._raw_text = raw_text
        self._configs = NLConfigManager()
        self._nlp = spacy.load(self._configs.spacy_core)
        self._vocabulary_units: list[VocabularyUnit] | None = None
        
        self._units_inflections: dict[VocabularyUnit, dict] | None = None
        
    
    def get_vocabulary_units(self) -> list[VocabularyUnit]:
        spacy_text = self._nlp(self._raw_text)
        self._vocabulary_units = sorted(set([VocabularyUnit(token.lemma_, token.pos_) for token in spacy_text
                                             if token.is_alpha and token.is_ascii]),
                                            key=lambda unit: unit.lemma)
        return self._vocabulary_units
    
    def get_all_inflections(self):
        if not self._vocabulary_units:
            self.get_vocabulary_units()
        self._units_inflections = {unit: inflections for unit in self._vocabulary_units
                                   if (inflections := lm.getAllInflections(unit.lemma, upos=unit.pos))}
        return self._units_inflections
    
    def save_inflections(self) -> None:
        if not self._units_inflections:
            self.get_all_inflections()
        with open(os.path.join(os.path.dirname(__file__), '../vocabularies/vocabulary.json'), 'w') as file:
            json.dump({unit.lemma: {'pos': unit.pos, 'inflections': self._units_inflections[unit]}
                       for unit in self._units_inflections}, file, indent=4)
