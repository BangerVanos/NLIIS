import spacy
import json
import benepar
import pymorphy3
from collections import Counter


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

    POS_TAGS = {
        'ADJ': 'Adjective',
        'ADP': 'Adposition',
        'ADV': 'Adverb',
        'AUX': 'Auxillary verb',
        'CCONJ': 'Coordinating conjunction',
        'DET': 'Determiner',
        'INTJ': 'Interjection',
        'NOUN': 'Noun',
        'NUM': 'Numeral',
        'PART': 'Particle',
        'PRON': 'Pronoun',
        'PROPN': 'Proper noun',
        'PUNCT': 'Punctuation',
        'SCONJ': 'Subordination conjunction',
        'SYM': 'Symbol',
        'VERB': 'Verb',
        'X': 'Other'
    }

    def __init__(self) -> None:
        self._en_nlp = spacy.load('en_core_web_sm')
        self._en_nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
        self._ru_nlp = spacy.load('ru_core_news_sm')
        self._ru_morph = pymorphy3.MorphAnalyzer()
        with open('./dict_en_ru.json', encoding='utf-8') as file:
            self._vocabulary = json.load(file)

    def translate(self, text: str):
        text_info = self._en_nlp(text)
        sentences = []
        sentences_statistics: list[dict] = []
        for sent in text_info.sents:
            sentence_statistics: dict[str, str | list[str, None] | dict] = self._translate_sent(sent.as_doc())
            sentence_statistics.update({'syntax_tree': sent._.parse_string, 'original': sent.text})            
            sentences.append(sentence_statistics['translation'])
            sentences_statistics.append(sentence_statistics)           
        word_frequency = dict(Counter([token.lemma_.lower() if not token.text == 'I' else token.text
                                       for token in text_info if token.is_alpha]))
        word_frequency = dict(sorted(list(word_frequency.items()), key=lambda i: i[1], reverse=True))
        word_pos = {token.lemma_: token.pos_ for token in text_info if token.is_alpha}
        return {
            'original_text': text,
            'translated_text': ' '.join(sentences),
            'statistics': sentences_statistics,
            'word_frequency': word_frequency,
            'word_pos': word_pos
        }
    
    def parse_statistics(self, statistics: dict) -> str:
        statistics_text: str = ""
        statistics_text += 'Original text:\n'
        statistics_text += f'{statistics["original_text"]}\n'
        statistics_text += f'{"-" * 30}\n'
        statistics_text += 'Translated text:\n'
        statistics_text += f'{statistics["translated_text"]}\n'
        statistics_text += f'{"-" * 30}\n'
        original_words_amount = sum([sentence['original_words_amount'] for sentence in statistics['statistics']])
        translated_words_amount = sum([sentence['translated_words_amount'] for sentence in statistics['statistics']])
        statistics_text += (
            f"Original text words amount: {original_words_amount}\n"
            f"Translated words amount: {translated_words_amount}\n"            
        )
        statistics_text += f'{"-" * 30}\n'
        statistics_text += 'Word statistics:\n'
        for word, freq in statistics['word_frequency'].items():
            pos = self.POS_TAGS.get(statistics['word_pos'].get(word), 'Unknown')
            translation = 'NONE' if self._vocabulary.get(word) in ('', None) else self._vocabulary.get(word) 
            statistics_text += f'{word} - {translation}. This word is {pos}, met {freq} times in text\n'
        return statistics_text
        
    def _translate_sent(self, sent_info) -> dict:
        translation: list[str | None] = []
        translated_words_amount = 0
        original_words_amount = 0
        for token in sent_info:            
            if token.is_alpha:
                original_words_amount += 1 
                if token.tag_ is None:
                    continue                
                lemma_trans = self._vocabulary.get(token.lemma_)
                if lemma_trans in (None, ''):
                    translation.append(None)
                    continue
                morph = self._ru_morph.parse(lemma_trans)[0]                                      
                morph.inflect({self.GRAMMEMES.get(en_grammeme) for en_grammeme in token.morph.to_dict().values()
                               if self.GRAMMEMES.get(en_grammeme) is not None})                
                translation.append(morph.word)
                translated_words_amount += 1
            else:
                translation.append(token.text)
        indexes = [ind for ind in range(len(translation)) if translation[ind] not in (None, "")]        
        clean_translation = [token for token in translation if token not in (None, "")]
        translation_string = ''       
        for ind, word in zip(indexes, clean_translation):
            translation_string += f' {word}' if not sent_info[ind].is_punct else word       
        return {
            'translation': translation_string.strip().capitalize(),
            'original_tokens': [token.text for token in sent_info],            
            'translated_tokens': translation,
            'original_words_amount': original_words_amount,
            'translated_words_amount': translated_words_amount           
        }
    
    def parse_vocabulary(self) -> str:
        parsed_vocabulary = ''        
        for word, trans in self._vocabulary.items():
            parsed_vocabulary += f'{word} - {trans}\n'            
        return parsed_vocabulary
    
    def update_vocabulary(self, new_words: dict[str, str] = {}) -> None:
        self._vocabulary.update(new_words)
        self._vocabulary = dict(sorted(list(self._vocabulary.items()),
                                       key=lambda i: i[0]))
        with open('./dict_en_ru.json', 'w', encoding='utf-8') as file:
            json.dump(self._vocabulary, file, indent=4, ensure_ascii=False)
    