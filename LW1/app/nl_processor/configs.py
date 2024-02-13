import json
import os


class NLConfigManager:

    def __init__(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), 'configs.json')) as file:
            self._configs = json.load(file)        

    @property
    def spacy_core(self) -> str:
        return self._configs['LANGUAGE_CORE_NAME']

    @property
    def possible_sentence_parts(self) -> dict:
        return self._configs['POSSIBLE_TAG_PART_OF_SENTENCE']    
