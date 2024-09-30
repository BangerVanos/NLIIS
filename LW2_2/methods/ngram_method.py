import json

from nltk import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer

import pandas as pd

with open('./methods/resources/ngram/ru_profile.json', encoding='utf-8') as file:
    ru_profile: dict = json.load(file)
with open('./methods/resources/ngram/en_profile.json', encoding='utf-8') as file:
    en_profile: dict = json.load(file)


def lang(text):
    vectorizer = CountVectorizer(analyzer='char',
                                 ngram_range=(5, 5),
                                 max_features=300)
    vectorizer.fit_transform(sent_tokenize(text))
    ngrams = vectorizer.get_feature_names_out()        

    ru_dist = 0        
    for i, ng in enumerate(ngrams):
        if ng in ru_profile:
            ru_dist += abs(ru_profile[ng] - i)
        else:
            ru_dist += 300

    en_dist = 0    
    for i, ng in enumerate(ngrams):
        if ng in en_profile:
            en_dist += abs(en_profile[ng] - i)
        else:
            en_dist += 300

    print(f'RU dist = {ru_dist}; EN dist = {en_dist}')

    if en_dist < ru_dist:
        return 'English'
    elif en_dist > ru_dist:
        return 'Russian'
    else:
        return 'Unable to recognize'
