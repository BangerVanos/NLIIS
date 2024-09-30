from bs4 import BeautifulSoup
import requests
import json
from translator import Translator


def make_translations_dict():
    rs = requests.get('http://www.7english.ru/dictionary.php?id=2000&letter=all')
    root = BeautifulSoup(rs.content, 'html.parser')

    en_ru_items = dict()    
    for tr in root.select('tr[onmouseover]'):
        td_list = [td.text.strip() for td in tr.select('td')]
        # Количество ячеек в таблице со словами — 9
        if len(td_list) != 9 or not td_list[1] or not td_list[5]:
            continue
        en = td_list[1]
        # Перевод английских слов предлагает несколько вариантов, мы берем первое слово из них
        ru = td_list[5].split(', ')[0]
        en_ru_items[en] = ru

    with open('dict_en_ru.json', 'w', encoding='utf-8') as file:
        json.dump(en_ru_items, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    tr = Translator()
    text = """I live in a house near the mountains. I have two brothers and one sister, and I was born last. My father teaches mathematics, and my mother is a nurse at a big hospital."""
    print(tr.translate(text))
    # make_translations_dict()