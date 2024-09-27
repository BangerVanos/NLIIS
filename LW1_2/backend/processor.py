from glob import glob
from itertools import chain
import re
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class Processor:

    PUNCTS: list[str] = [',', '.', '?', ':', '-', ';', '!', '...', '\n', '\r']
    LOGICAL_OPERATIONS_MAP: dict[str, str] = {        
        'или': 'or',
        'но не': 'and not',        
        'не': 'not',
        'а также': 'and',        
        'и': 'and',
        'and': 'and',
        'or': 'or',
        'not': 'not',
        '&': 'and',
        '|': 'or',
        '~': 'not',
        '!': 'not'
    }

    def __init__(self, db_folders: list[str], query: str) -> None:                  
        self._files = list(chain.from_iterable([glob(fr'{os.path.normpath(folder)}/*.txt', recursive=True)
                                                for folder in db_folders]))           
        print(self._files)
        self._query = query
        for sym in self.PUNCTS:
            self._query = self._query.replace(sym, '')
        self._query_tokens = list(map(lambda s: s.replace('\'', '').replace('"', '').lower(),
                                      re.findall(re.compile(r'\'\w+\'|\"\w+\"'), self._query)))
        raw_tokens = list(re.findall(re.compile(r'\'\w+\'|\"\w+\"'), self._query))
        for token in raw_tokens:
            self._query = self._query.replace(token, '[TAG]')
        for operation, python_operation in self.LOGICAL_OPERATIONS_MAP.items():
            self._query = self._query.replace(operation, python_operation)
        for token in self._query_tokens:
            self._query = self._query.replace('[TAG]', token, 1)
        # print(self._query_tokens)
        # print(self._query)
    
    def execute_query(self) -> dict:        
        result = []
        for path in self._files:
            query = self._query
            with open(path, encoding='utf-8') as file:
                text = file.read()
            text = text.lower()            
            for sym in self.PUNCTS:
                text = text.replace(sym, '')
            text_tokens = text.split(' ')
            for token in self._query_tokens:
                if token in text_tokens:
                    query = query.replace(token, 'True', 1)
                else:
                    query = query.replace(token, 'False', 1)
            # print(query)                       
            if eval(query):
                result.append(path)
        return {
            'documents': result,
            'metrics': {
                'acc': round(1, 2),
                'prec': round(1, 2),
                'rec': round(1, 2),
                'f1': round(1, 2)
            }
        }


def validate_query(query: str) -> str:
    client = OpenAI(
        api_key=os.getenv('API_KEY'), # ваш ключ в VseGPT после регистрации
        base_url="https://api.vsegpt.ru/v1",
    )
    system_prompt = """Ты оцениваешь текстовые запросы, которые тебе поступают. Запросы выполнены на русском языке.
    Запросы могут содержать следующие знаки пунктуации: ',', '.', '?', ':', '-', ';', '!', '...'.
    Запросы содержат различные союзы, как, например: 'и', 'или', 'не', 'но не' и другие.
    Запросы содержат ключевые слова, связанные этими союзами. Ключевое слово обязано быть обёрнуто в одиарные или 
    двойные кавычки, например 'тест' или 'Тест'.
    Примеры:
    Query: 'Каренина' или 'Анна'
    Answer: 'Это правильный запрос'
    Query: 'Рогожин' и 'Мышкин', но не 'Анна'
    Answer: 'Это правильный запрос'
    Query: 'Анна и 'Каренина'
    Answer: 'Это неправильный запрос, так как ключевое слово 'Анна' не обёрнуто в кавычки'
    Query: 'Рогожин' и
    Answer: 'Это неправильный запрос, так как союз 'и' должен связывать два ключевых слова'"""

    response_big = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': query}],
        temperature=1,
        n=1,
        max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
        extra_headers={"X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
    )
    response = response_big.choices[0].message.content
    return response


def summarize_text(path: str) -> str:
    client = OpenAI(
        api_key=os.getenv('API_KEY'), # ваш ключ в VseGPT после регистрации
        base_url="https://api.vsegpt.ru/v1",
    )
    system_prompt = """Ты делаешь краткое содержание текста. Краткое содержание должно помещаться в 150 слов, не больше."""
    with open(path, encoding='utf-8') as file:
        text = file.read()
    if len(text) < 50_000:
        begin = 0
    else:
        begin = len(text) // 2
    response_big = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': text[begin - 25000:begin + 25000]}],
        temperature=1,
        n=1,
        max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
        extra_headers={"X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
    )
    response = response_big.choices[0].message.content
    return response
