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
    
    def save_inflections(self, global_vocabulary: bool = False) -> None:
        '''Save all inflections to file for later use. If global_vocabulary is True,
        all of new inflections will be added to global big vocabulary, which you can shape
        from different text files'''

        if not self._units_inflections:
            self.get_all_inflections()
        text_vocabulary: dict = {unit.lemma: {'pos': unit.pos, 'inflections': self._units_inflections[unit],
                                              'sentence_part': self._configs.possible_sentence_parts[unit.pos]}
                                 for unit in self._units_inflections}
        with open(os.path.join(os.path.dirname(__file__), '../vocabularies/vocabulary.json'), 'w') as file:
            json.dump(text_vocabulary, file, indent=4)
        if global_vocabulary:
            with open(os.path.join(os.path.dirname(__file__),
                                   '../vocabularies/global_vocabulary.json'), 'w+') as file:
                try:
                    vocabulary = json.load(file)
                except json.JSONDecodeError:
                    vocabulary = {}
                vocabulary.update(text_vocabulary)
                vocabulary = dict(sorted(vocabulary.items()))
                json.dump(vocabulary, file, indent=4)
