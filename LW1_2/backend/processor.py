import os
import re
from itertools import groupby
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

# Карта логических операций: преобразует строковые операции в логические функции
str_to_token = {
    '1': True,  # Истина
    '0': False,  # Ложь
    'AND': lambda left, right: left and right,  # Логическое "И"
    'OR': lambda left, right: left or right,  # Логическое "ИЛИ"
    'NOT': lambda right: not right,  # Логическое "НЕ"
    '(': '(',  # Открывающая скобка
    ')': ')'   # Закрывающая скобка
}

empty_res = True  # Значение по умолчанию, если выражение пустое

def create_token_lst(s, str_to_token=str_to_token):
    """
    Преобразует строку логического выражения в список токенов для дальнейшей обработки.

    Args:
        s (str): Логическое выражение в виде строки.
        str_to_token (dict): Словарь для преобразования строк в токены.

    Returns:
        list: Список токенов.
    """
    s = s.replace('(', ' ( ')  # Добавляем пробелы вокруг скобок
    s = s.replace(')', ' ) ')
    return [str_to_token[it] for it in s.split()]  # Преобразуем строку в список токенов

def find(lst, what, start=0):
    """
    Ищет индексы элементов в списке, которые совпадают с заданным элементом начиная с определенной позиции.

    Args:
        lst (list): Список, в котором выполняется поиск.
        what: Элемент для поиска.
        start (int, optional): Индекс, с которого начинать поиск. По умолчанию 0.

    Returns:
        list: Список индексов найденных элементов.
    """
    return [i for i, it in enumerate(lst) if it == what and i >= start]

def parens(token_lst):
    """
    Находит самую глубокую вложенную пару скобок в списке токенов.

    Args:
        token_lst (list): Список токенов.

    Returns:
        tuple: Кортеж, содержащий флаг наличия скобок, индекс открывающей скобки, индекс закрывающей скобки.
    """
    left_lst = find(token_lst, '(')
    if not left_lst:
        return False, -1, -1
    left = left_lst[-1]
    # Поиск закрывающей скобки
    right = find(token_lst, ')', left + 3)[0] if token_lst[left + 1] != 0 and token_lst[left + 1] != 1 else find(token_lst, ')', left + 4)[0]
    return True, left, right

def bool_eval(token_lst):
    """
    Оценивает булевое выражение без скобок.

    Args:
        token_lst (list): Список токенов для оценки.

    Returns:
        bool: Результат булевого выражения.
    """
    if len(token_lst) == 2:  # Если это операция NOT
        return token_lst[0](token_lst[1])
    return token_lst[1](token_lst[0], token_lst[2])  # Выполняем операцию AND/OR

def formatted_bool_eval(token_lst, empty_res=empty_res):
    """
    Рекурсивно оценивает булевое выражение, учитывая скобки.

    Args:
        token_lst (list): Список токенов для оценки.
        empty_res (bool, optional): Значение по умолчанию, если выражение пустое.

    Returns:
        bool: Результат булевого выражения.
    """
    if not token_lst:
        return empty_res
    if len(token_lst) == 1:
        return token_lst[0]  # Если в выражении только одно значение
    has_parens, l_paren, r_paren = parens(token_lst)
    if not has_parens:
        return bool_eval(token_lst)  # Если нет скобок
    token_lst[l_paren:r_paren + 1] = [bool_eval(token_lst[l_paren + 1:r_paren])]  # Обрабатываем выражение в скобках
    return formatted_bool_eval(token_lst, bool_eval)

def nested_bool_eval(s):
    """
    Выполняет полную оценку логического выражения, включая скобки.

    Args:
        s (str): Логическое выражение в виде строки.

    Returns:
        bool: Результат оценки выражения.
    """
    return formatted_bool_eval(create_token_lst(s))

def find_word(word, base_dir='.'):
    """
    Ищет заданное слово во всех файлах указанной директории.

    Args:
        word (str): Слово для поиска.
        base_dir (str, optional): Директория для поиска. По умолчанию текущая директория.

    Returns:
        str: '1', если слово найдено, иначе '0'.
    """
    result = 0
    for root, _, files in os.walk(base_dir, topdown=False):
        for name in files:
            with open(os.path.join(root, name), encoding='utf-8') as file:
                if any(word in line for line in file):
                    result = 1
    return str(result)

def find_word_in_file(file, word, words_list):
    """
    Ищет слово в конкретном файле и добавляет его в список, если оно найдено.

    Args:
        file (str): Путь к файлу для поиска.
        word (str): Слово для поиска.
        words_list (list): Список для хранения найденных слов.

    Returns:
        str: '1', если слово найдено, иначе '0'.
    """
    result = 0
    with open(file, encoding='utf-8') as file:
        if any(word in line for line in file):
            result = 1
            words_list.append(word)
    return str(result)

def find_in_dir(text, base_dir='.'):
    """
    Выполняет поиск слов, указанных в логической формуле, по всем файлам в директории.

    Args:
        text (str): Логическая формула для поиска.
        base_dir (str, optional): Директория для поиска. По умолчанию текущая директория.

    Returns:
        None
    """
    all_rsv = []
    all_truth = []
    docs: list[str] = []
    for root, _, files in os.walk(base_dir, topdown=False):
        for name in files:
            words_list = []
            pattern = re.compile(r"'(.*?)'", re.S)  # Регулярное выражение для поиска слов в кавычках
            file_search_str = re.sub(pattern, lambda m: find_word_in_file(os.path.join(root, name), m.group(1), words_list=words_list), text)
            rsv = nested_bool_eval(file_search_str)  # Оценка логической формулы
            new_words_list = [el for el, _ in groupby(words_list)]  # Убираем дубликаты из списка слов
            all_rsv.append(int(rsv))
            all_truth.append(1 if new_words_list else 0)  # Истина, если слова найдены
            if rsv:
                docs.append(os.path.abspath(os.path.join(root, name)))
                # print("Файл: " + os.path.abspath(os.path.join(root, name)) + "\nСписок присутствующих слов: " + str(new_words_list))

    # Вычисление метрик поиска
    acc = accuracy_score(all_truth, all_rsv)
    prec = precision_score(all_truth, all_rsv, zero_division=0)
    rec = recall_score(all_truth, all_rsv)
    f1 = f1_score(all_truth, all_rsv)

    return {
        'documents': docs,
        'metrics': {
            'acc': round(acc, 2),
            'prec': round(prec, 2),
            'rec': round(rec, 2),
            'f1': round(f1, 2)
        }
    }
