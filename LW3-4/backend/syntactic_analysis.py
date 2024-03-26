import benepar, spacy


class SyntacticAnalysis:

    def __init__(self) -> None:
        self._nlp = spacy.load('en_core_web_md')
        self._nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
    
    def build_syntac_trees(self, text: str):
        parser = self._nlp(text)
        result = {}
        for sent in parser.sents:
            level = 1
            
            