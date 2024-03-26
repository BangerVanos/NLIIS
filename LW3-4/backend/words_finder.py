import spacy as sp


class WordsFinder:

    def __init__(self) -> None:
        self._nlp = sp.load('en_core_web_md')
    
    def find_words(self, text: str) -> list[str]:
        tokens = self._nlp(text)
        return sorted(set(
            [token.lower_ if token.pos_ != 'PROPN' else token.text
             for token in tokens if token.is_alpha and token.is_ascii]
        ))
