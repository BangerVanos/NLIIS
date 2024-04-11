import benepar, spacy
import os
import json


class SyntacticAnalysis:

    def __init__(self) -> None:
        self._nlp = spacy.load('en_core_web_md')
        self._nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    
    def build_syntax_trees(self, text: str, save: bool = True):
        parser = self._nlp(text)
        result = {}
        for sent in parser.sents:            
            result[id(str(sent))] = {
                'raw_sentence': str(sent),
                'penn_treebank': sent._.parse_string                              
            }
        
        if save:
            self._save_to_json(result)

        return result

    def _save_to_json(cls, result: dict) -> None:
        with open(os.path.realpath(os.path.join(
            os.path.dirname(__file__), 'analysis_records/syntactic_analysis.json'
        )), 'w') as file:
            json.dump(result, file, indent=4) 
            