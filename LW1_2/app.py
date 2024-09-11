import streamlit as st
import streamlit_shadcn_ui as ui
from backend.processor import find_in_dir


def main():    
    st.set_page_config(page_title='Логический поиск в файлах', 
                       layout='wide')
    st.header('1. Введите путь к папке с документами')
    docs =st.text_input(label='Путь к папке', key='docs_path')
    st.header('2. Введите логическое выражение')
    with st.expander('Пояснение к синтаксису логических запросов'):
        st.text(
            """Вложенность логического запроса регулируется скобками (т.е. для нового уровня вложенности подвыражение обрамляется круглыми скобками)
            Поддерживаемые логические операторы:
            AND - логическое И
            OR - логическое ИЛИ
            NOT - логическое НЕ
            Выражения для поиска обрамляются одинарными кавычками (например, 'Текст')"""
        )
    query = st.text_input(label='Запрос', key='query')
    st.header('3. Провести поиск по документам')
    btn = ui.button('Провести поиск', variant='default', key='btn')
    metrics_chk = ui.checkbox(label='Показать метрики?', key='metrics_chk')
    if btn:
        if not docs:
            st.error('Укажите путь к папке с документами!')
        if not query:
            st.error('Введите поисковое выражение!')
        else:
            result = find_in_dir(query, docs)
            st.session_state['result'] = result           
            st.write('## Релевантные документы:')
            for doc in result['documents']:
                st.write(f'#### {doc}')            
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
    main()
