import streamlit as st
import streamlit_shadcn_ui as ui
from backend.ex_processor import find_in_dir
from backend.processor import Processor
from backend.processor import validate_query, summarize_text
from streamlit_extras.stateful_button import button
from io import StringIO
import os
from random import randint


def main():    
    st.set_page_config(page_title='Логический поиск в файлах', 
                       layout='wide')
    st.header('1. Введите путь к папке с документами')
    docs = st.file_uploader(label='Путь к конфигурационному файлу', key='docs_path', type='txt',
                            help='Данный документ формата .txt должен содержать пути к папкам с документами на устройствах сети')
    st.header('2. Введите логическое выражение')
    with st.expander('Пояснение к синтаксису логических запросов'):
        st.text(
            """Вложенность логического запроса регулируется скобками (т.е. для нового уровня вложенности подвыражение обрамляется круглыми скобками)
            Поддерживаемые союзы и частицы: 'и', 'или', 'не', 'но не', 'а также'
            Выражения для поиска обрамляются одинарными кавычками (например, 'Текст').
            После введения запроса его можно проверить на правильность, нажав на кнопку 'Проверить запрос на правильность'.
            При нажатии на эту кнопку интеллектуальный агент проверит правильность синтаксиса вашего запроса.
            Пример правильного запроса: 'Анна' или 'Каренина'"""
        )
    query = st.text_input(label='Запрос', key='query')
    if query:
        ask_btn = st.button(label='Проверить запрос на правильность', key='ask_btn')
        if ask_btn:
            validate_answer = validate_query(query)
            st.info(validate_answer)
    st.header('3. Провести поиск по документам')
    btn = button('Провести поиск', type='secondary', key='btn')
    metrics_chk = st.checkbox(label='Показать метрики?', key='metrics_chk')
    if btn:
        if not docs:
            st.error('Укажите путь к конфигурационному файлу!')
        if not query:
            st.error('Введите поисковое выражение!')
        else:
            dbs: list[str] = StringIO(docs.getvalue().decode('utf-8')).read().split('\n')
            dbs = [folder.replace('\n', '').replace('\r', '').replace(os.sep, '/') for folder in dbs]            
            proc = Processor(dbs, query)
            result = proc.execute_query()
            st.session_state['result'] = result           
            st.write('## Релевантные документы:')
                        
            for doc in result['documents']:
                with st.expander(label=doc):                

                    st.write('Гиперссылка на документ')                
                    st.write(f'<p><a href=file://localhost/{doc}>{doc}</a></p>', unsafe_allow_html=True)                    
                    sum_btn = st.button(f'Привести краткое содержание текста документа', key=f'sum_{doc}')                                    

                    if sum_btn:
                        text_sum = summarize_text(doc)
                        st.info(text_sum)       
            if metrics_chk:
                st.write('## Метрики:')
                text = (
                    f'Accuracy: {result['metrics']['acc']}\n\n'
                    f'Precision: {result['metrics']['prec']}\n\n'
                    f'Recall: {result['metrics']['rec']}\n\n'
                    f'F1-score: {result['metrics']['f1']}'
                )                
                st.write(text)


if __name__ == "__main__":
    # (('Здравствуйте' AND 'легенда') OR (NOT 'пора'))
    # (('Рогожин' AND 'Мышкин') OR 'Каренина')
    # (NOT 'смартфон')
    # ('смартфон' AND 'телефон')
    main()
