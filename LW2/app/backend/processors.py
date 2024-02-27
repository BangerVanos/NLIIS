import pandas as pd
from glob import glob
import os
import spacy

class TextCoprusProcessor:

    def __init__(self, load_existing=False) -> None:
        self._load_existing = load_existing
        if not load_existing:
            self._result_df = pd.DataFrame(columns=['word',
                                                    'lemma',
                                                    'part_of_speech',
                                                    'tag'])
        else:
            self._result_df = self._load_ready()
        self._temp_df_list = []
        spacy.prefer_gpu()
        self._nlp = spacy.load('en_core_web_md')
    
    def _parse_text_corpus(self) -> None:
        for file_path in glob(os.path.realpath(os.path.join(
            os.path.dirname(__file__), 'text_corpus/*.txt'
        ))):
            with open(file_path, encoding='utf-8') as file:
                line_count = 0
                for line in file:                     
                    parsed_line = self._nlp(line.strip('\n'))
                    new_words = {
                        'word': [token.text.lower() if not token.pos_ == 'PROPN' 
                                 else token.text for token in parsed_line if token.is_ascii and token.is_alpha],
                        'lemma': [token.lemma_ for token in parsed_line if token.is_ascii and token.is_alpha],
                        'part_of_speech': [token.pos_ for token in parsed_line if token.is_ascii and token.is_alpha],
                        'tag': [token.tag_ for token in parsed_line if token.is_ascii and token.is_alpha]
                    }
                    temp_df = pd.DataFrame(new_words)
                    self._temp_df_list.append(temp_df)
                    line_count += 1
                    if line_count % 1000 == 0:
                        self._result_df = pd.concat([self._result_df] + self._temp_df_list)
                        self._temp_df_list.clear() 
       
    def process_text_corpus(self) -> None:
        if not self._load_existing:
            self._parse_text_corpus()
            self._result_df.to_csv(os.path.realpath(os.path.join(
                os.path.dirname(__file__), 'text_corpus_stats/result.csv')), index=False)
        self._create_lemma_stats()
        self._create_word_stats()
        self._create_pos_stats()
        self._create_tag_stats()
    
    def _create_lemma_stats(self) -> None:
        pass

    def _create_word_stats(self) -> None:
        pass

    def _create_pos_stats(self) -> None:
        pass

    def _create_tag_stats(self) -> None:
        pass
    
    def _load_ready(self) -> pd.DataFrame:
        return pd.read_csv(os.path.realpath(os.path.join(
                           os.path.dirname(__file__),
                           'text_corpus_stats/result.csv')),
                          )
