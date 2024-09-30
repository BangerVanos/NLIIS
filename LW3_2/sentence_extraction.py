import nltk
import math
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from tqdm import tqdm

# Функция для вычисления tf(t, D)
def term_frequency(term, doc, tf_max_d_text):
    # words = word_tokenize(tf_max_d_text)
    return tf_max_d_text.count(term) / len(tf_max_d_text)

# Функция для вычисления df(t) — в скольких документах встречается термин t
def document_frequency(term, corpus):
    return sum(1 for doc in corpus if term in word_tokenize(doc.lower()))

# Функция для вычисления веса термина по модифицированной формуле
def compute_tfidf_weight(term, doc, corpus, tf_max_d_text):
    tf_t_d = term_frequency(term, doc, tf_max_d_text)
    tf_max_d = max(term_frequency(word, doc, tf_max_d_text) for word in tf_max_d_text)
    df_t = document_frequency(term, corpus)
    db_size = len(corpus)
    
    return 0.5 * (1 + tf_t_d / tf_max_d) * math.log(db_size / (df_t + 1))

# Функция для вычисления позиции предложения в документе
def calculate_posd(sentence_index, doc_length):
    return 1 - sentence_index / doc_length

# Функция для вычисления позиции предложения в абзаце
def calculate_posp(sentence_index, para_length):
    return 1 - sentence_index / para_length

# Функция для вычисления веса предложений
def compute_sentence_scores(sentences, corpus, stop_words):
    scores = []
    # print(len(sentences))


    tf_max_d_text = word_tokenize(' '.join(sentences).lower(), language='russian')
    for i, sentence in enumerate(sentences):
        # Убираем стоп-слова и токенизируем предложение
        words = [word for word in word_tokenize(sentence.lower(), language='russian') if word.isalnum() and word not in stop_words]
        
        # Суммируем веса слов (модифицированный TF-IDF)
        score = 0
        for word in words:
            tfidf_score = compute_tfidf_weight(word, ' '.join(sentences), corpus, tf_max_d_text)
            score += tfidf_score
        
        # Учитываем положение предложения в документе и абзаце
        posd = calculate_posd(i, len(sentences))
        posp = calculate_posp(i, len(sentences))
        
        # Итоговый вес предложения
        final_score = score * posd * posp
        scores.append((sentence, final_score))
    
    return scores

# Основная функция для генерации реферата
def generate_summary(text, n=10, language='russian'):
    stop_words = set(stopwords.words(language))
    
    # Токенизация текста на предложения
    sentences = sent_tokenize(text)
    
    # Формируем корпус из текста
    corpus = [text]
    
    # Вычисляем веса предложений
    sentence_scores = compute_sentence_scores(sentences, corpus, stop_words)

    print('Done 2')
    
    # Сортировка предложений по весу
    sorted_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
    
    # Выбор n лучших предложений
    summary = [sentence for sentence, score in sorted_sentences[:n]]
    
    # Сортируем предложения по порядку их появления в тексте
    summary = sorted(summary, key=lambda x: sentences.index(x))
    
    return ' '.join(summary)
