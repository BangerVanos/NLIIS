from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()


def ml_extraction(text: str, min_length: int = 100, max_length: int = 512) -> str:
    system_prompt = (f"""
    You are text summarizing model. You can summarize texts in Russian and English languages.
    Minimal length of result is {min_length} symbols.
    Maximal length of result is {max_length} symbols.
    Provide only result, without additional comments of yours.
    """)
    
    client = OpenAI(
        api_key=os.getenv('API_KEY'), # ваш ключ в VseGPT после регистрации
        base_url="https://api.vsegpt.ru/v1",
    )
    response_big = client.chat.completions.create(
        model="openai/gpt-4o-mini", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
        messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': text}],
        temperature=1,
        n=1,
        max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
        extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
    )   
    response = response_big.choices[0].message.content
    return response
