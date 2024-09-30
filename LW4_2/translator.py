import spacy
import json
import pymorphy3
from lemminflect import getInflection


class Translator:

    GRAMMEMES = {
        'Nom': 'nomn',
        'Gen': 'gent',
        'Dat': 'datv',
        'Acc': 'accs',
        'Abs': 'ablt',
        'Loc': 'loct',
        'Voc': 'voct',
        'Sing': 'sing',
        'Plur': 'plur',
        'Fem': 'femn',
        'Masc': 'masc',
        'Neut': 'neut',        
    }

    def __init__(self) -> None:
        self._en_nlp = spacy.load('en_core_web_sm')
        self._ru_nlp = spacy.load('ru_core_news_sm')
        self._ru_morph = pymorphy3.MorphAnalyzer()
        with open('./dict_en_ru.json', encoding='utf-8') as file:
            self._vocabulary = json.load(file)

    def translate(self, text: str):
        text_info = self._en_nlp(text)
        sentences = []
        for sent in text_info.sents:
            sentences.append(self._translate_sent(sent.as_doc()))
        return ' '.join(sentences)
    
    def _translate_sent(self, sent_info):
        translation: list[str | None] = []
        for token in sent_info:            
            if token.is_alpha:                
                lemma_trans = self._vocabulary.get(token.lemma_)
                if lemma_trans in (None, '') or token.tag_ is None:
                    continue
                morph = self._ru_morph.parse(lemma_trans)[0]
                print(token.morph)                      
                morph.inflect({self.GRAMMEMES.get(en_grammeme) for en_grammeme in token.morph.to_dict().values()
                               if self.GRAMMEMES.get(en_grammeme) is not None})                
                translation.append(morph.word)
            else:
                translation.append(token.text)
        translation = [token for token in translation if token not in (None, "")]
        return (' '.join(translation[:-1]) + f'{"" if sent_info[-1].is_punct else " "}{translation[-1]}').capitalize()




