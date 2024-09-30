import streamlit as st
from sentence_extraction import generate_summary
from keyphrases_extraction import keyphrases_extraction
from ml_extraction import ml_extraction
from io import StringIO
import os


st.set_page_config(page_title='Summarization App',
                   layout='wide')

def app():
    st.header('### Choose texts\' language')
    language = st.selectbox(label='Select text\' language',
                            key='language',
                            options=['russian', 'english'],
                            format_func=lambda l: {'russian':'Russian', 'english':'English'}[l])
    st.header('### Upload documents with texts')
    uploaded_docs = st.file_uploader(label='Upload text documents',
                                     type='txt', key='raw_docs',
                                     accept_multiple_files=True)
    docs: dict[str, str] = {}     
    for raw_doc in uploaded_docs:
        stringio = StringIO(raw_doc.getvalue().decode('utf-8'))
        text = stringio.read()
        name = os.path.splitext(os.path.basename(raw_doc.name))[0]
        docs[name] = text
        with open(f'./texts/{raw_doc.name}', 'w', encoding='utf-8') as file:
            file.write(text)
    sum_btn = st.button(label='Get texts\' summarizations',
                        type='primary', key='sum_btn')
    if sum_btn:
        result: dict[str, dict] = {}
        for name, text in docs.items():
            path = f'{os.path.dirname(__file__).replace(os.sep, '/')}/texts/{name}.txt'
            result[path] = {}
            keyphrases = keyphrases_extraction(text, language, 10)
            with open(f'./results/{name}_keyphrases.txt', 'w', encoding='utf-8') as file:
                file.write('\n'.join(keyphrases))
                
            sentences = generate_summary(text, 10, language)
            with open(f'./results/{name}_sentences.txt', 'w', encoding='utf-8') as file:
                file.write(sentences)
                
            ml = ml_extraction(text, min_length=100, max_length=250)
            with open(f'./results/{name}_ml.txt', 'w', encoding='utf-8') as file:
                file.write(ml)            
            
            result[path]['keyphrases'] = f'{os.path.dirname(__file__).replace(os.sep, '/')}/results/{name}_keyphrases.txt'
            result[path]['sentences'] = f'{os.path.dirname(__file__).replace(os.sep, '/')}/results/{name}_sentences.txt'
            result[path]['ml'] = f'{os.path.dirname(__file__).replace(os.sep, '/')}/results/{name}_ml.txt'

            # Rendering result
            with st.expander(f'{name}.txt'):
                st.write('Document hyperlink')
                st.write(f'<p><a href=file://localhost/{path}>{name}.txt</a></p>', unsafe_allow_html=True)
                st.write('Keyphrases')
                with st.container(border=True):
                    st.write('; '.join(keyphrases))
                st.write('Keyphrases document hyperlink')                
                st.write(f'<p><a href=file://localhost/{result[path]["keyphrases"]}>{name}_keyphrases.txt</a></p>', unsafe_allow_html=True)
                st.write('Main sentences')
                with st.container(border=True):
                    st.write(sentences)
                st.write('Main sentences document hyperlink')
                st.write(f'<p><a href=file://localhost/{result[path]["sentences"]}>{name}_sentences.txt</a></p>', unsafe_allow_html=True)
                st.write('ML summarization')
                with st.container(border=True):
                    st.write(ml)
                st.write('ML summarization document hyperlink')
                st.write(f'<p><a href=file://localhost/{result[path]["ml"]}>{name}_ml.txt</a></p>', unsafe_allow_html=True)

    # name_file
    # гипер ссылка на этот файл
    # и тут 3 ссылки на новые доки по этому файлу


if __name__ == '__main__':
    app()
