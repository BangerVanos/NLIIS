from sklearn.feature_extraction.text import CountVectorizer
import requests
from bs4 import BeautifulSoup
from nltk import sent_tokenize
import json
from tqdm import tqdm

def get_russian_profile():
    vectorizer = CountVectorizer(ngram_range=(5, 5), analyzer='char',
                                 max_features=300)
    with open('russian_texts.txt', encoding='utf-8') as file:
        urls = file.readlines()
    texts: list[str] = []    
    for url in tqdm(urls):
        result = requests.get(url)
        if result.status_code == 200:
            html = result.text
        else:
            html = None
        if html is None:
            continue
        soup = BeautifulSoup(html, features='html.parser')
        clean_text = soup.get_text('\n', strip=True)
        texts.extend(sent_tokenize(clean_text, language='russian'))
    vectorizer.fit_transform(texts)
    ngrams = vectorizer.get_feature_names_out()
    with open('ru_profile.json', 'w', encoding='utf-8') as file:
        json.dump(dict(zip(ngrams, range(300))), file, ensure_ascii=False, indent=4)



def get_english_profile():
    vectorizer = CountVectorizer(ngram_range=(5, 5), analyzer='char',
                                 max_features=300)
    with open('english_texts.txt', encoding='utf-8') as file:
        urls = file.readlines()
    texts: list[str] = []    
    for url in tqdm(urls):
        result = requests.get(url)
        if result.status_code == 200:
            html = result.text
        else:
            html = None
        if html is None:
            continue
        soup = BeautifulSoup(html, features='html.parser')
        clean_text = soup.get_text('\n', strip=True)
        texts.extend(sent_tokenize(clean_text, language='english'))
    vectorizer.fit_transform(texts)
    ngrams = vectorizer.get_feature_names_out()
    with open('en_profile.json', 'w', encoding='utf-8') as file:
        json.dump(dict(zip(ngrams, range(300))), file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # get_russian_profile()
    get_english_profile()