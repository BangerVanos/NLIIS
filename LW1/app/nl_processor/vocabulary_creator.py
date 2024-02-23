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
                                            key=lambda unit: unit.lemma.lower())
        return self._vocabulary_units
    
    def get_all_inflections(self):
        if not self._vocabulary_units:
            self.get_vocabulary_units()
        self._units_inflections = {unit: inflections for unit in self._vocabulary_units
                                   if (inflections := lm.getAllInflections(unit.lemma, upos=unit.pos))}
        return self._units_inflections
    
    def save_inflections(self, save_to_global_vocabulary: bool = False,
                         use_global_vocabulary: bool = False) -> None:
        '''Save all inflections to file for later use. If global_vocabulary is True,
        all of new inflections will be added to global big vocabulary, which you can shape
        from different text files. If use_global_vocabulary is True, lemmas from global
        vocabulry will have higher priority of filling text's vocabulry.'''

        if not self._units_inflections:
            self.get_all_inflections()      
        
        text_vocabulary: dict = {unit.lemma: {'pos': unit.pos, 'inflections': self._units_inflections[unit],
                                              'sentence_part': self._configs.possible_sentence_parts[unit.pos],
                                              'creation_type': 'machinery'}
                                 for unit in self._units_inflections}
        VocabularyRepository.save_to_vocabulary(text_vocabulary, use_global_vovabulary=use_global_vocabulary)

        if save_to_global_vocabulary:
            VocabularyRepository.save_to_global_vocabulary(text_vocabulary, use_manual_over_machinery=True)


class VocabularyRepository:

    @classmethod
    def load_temp_vocabulary(cls) -> dict:
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                  f'..{os.sep}vocabularies{os.sep}vocabulary.json'))) as file:
            try:
                vocabulary = json.load(file)
            except json.JSONDecodeError:
                vocabulary = {}
        return vocabulary
    
    @classmethod
    def load_global_vocabulary(cls) -> dict:
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                  f'..{os.sep}vocabularies{os.sep}global_vocabulary.json'))) as file:
            try:
                vocabulary = json.load(file)
            except json.JSONDecodeError:
                vocabulary = {}
        return vocabulary
    
    @classmethod
    def _save_to_global_vocabulary_force(cls, saved_vocabulary: dict) -> None:
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                  f'..{os.sep}vocabularies{os.sep}global_vocabulary.json')), 'w') as file:
            json.dump(saved_vocabulary, file, indent=4)
    
    @classmethod
    def _save_to_temp_vocabulary_force(cls, saved_vocabulary: dict) -> None:
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                  f'..{os.sep}vocabularies{os.sep}vocabulary.json')), 'w') as file:
            json.dump(saved_vocabulary, file, indent=4)

    
    @classmethod
    def save_to_vocabulary(cls, vocabulary: dict, use_global_vovabulary: bool = False) -> None:
        saved_vocabulary = {}
        if use_global_vovabulary:
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                      f'..{os.sep}vocabularies{os.sep}global_vocabulary.json'))) as file:
                try:
                    global_vocabulary = json.load(file)
                except json.JSONDecodeError:
                    global_vocabulary = {}
            saved_vocabulary_lemmas = list(vocabulary.keys())
            [saved_vocabulary.setdefault(lemma, global_vocabulary[lemma]) for lemma in
             saved_vocabulary_lemmas if lemma in global_vocabulary]            
        saved_vocabulary.update(vocabulary)
        cls._save_to_temp_vocabulary_force(saved_vocabulary)
    
    @classmethod
    def save_to_global_vocabulary(cls, vocabulary: dict, use_manual_over_machinery: bool = True) -> None:
        '''Saves new lemmas to global vocabulary. If use_manual_over_machinery is True, lemmas
        made manually (by user) will be saved over ones which were created automatically'''
        saved_vocabulary = cls.load_global_vocabulary()        
        if use_manual_over_machinery:
            [saved_vocabulary.setdefault(lemma, info) for lemma, info in saved_vocabulary.items()
             if info['creation_type'] == 'manual']
            [saved_vocabulary.setdefault(lemma, info) for lemma, info in vocabulary.items()
             if info['creation_type'] == 'manual']
        saved_vocabulary.update(vocabulary)
        cls._save_to_global_vocabulary_force(saved_vocabulary)
    
    
    @classmethod
    def update_vocabulary(cls, updated_lemmas: dict) -> None:
        cls.save_to_global_vocabulary(updated_lemmas, use_manual_over_machinery=False)
    
    @classmethod
    def modify_vocabulary(cls, modified_lemmas: dict | list, delete_only: bool = False) -> None:
        modified_vocabulary = cls.load_global_vocabulary()
        modified_lemmas_without_info = (modified_lemmas.keys() if isinstance(modified_lemmas, dict)
                                        else modified_lemmas)
        [modified_vocabulary.pop(lemma) for lemma in modified_lemmas_without_info
         if lemma in modified_vocabulary]
        cls._save_to_global_vocabulary_force(modified_vocabulary)
        if delete_only:
            return
        cls.update_vocabulary(modified_lemmas)

    @classmethod
    def filter_vocabulary(cls, vocabulary: dict, lemma: str | None = None, pos: str | None = None,
                                 part_of_sentence: str | None = None):
        if lemma:
            vocabulary = dict(filter(lambda pair: lemma.lower()
                                     in pair[0].lower(), vocabulary.items()))        
        if pos:            
            vocabulary = dict(filter(lambda pair: 
                                     pos.lower().startswith(pair[1]['pos'].lower()),                                                                        
                                     vocabulary.items()))        
        if part_of_sentence:
            vocabulary = dict(filter(lambda pair: part_of_sentence.lower()
                                     in pair[1]['sentence_part'], vocabulary.items()))
        return dict(sorted(vocabulary.items(), key=lambda item: item[0].lower()))       
