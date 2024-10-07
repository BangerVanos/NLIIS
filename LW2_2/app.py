import streamlit as st
from methods.alphabetic_method import lang as alphabetic_language
from methods.neural_method import lang as neural_language
from methods.ngram_method import lang as ngram_language
import requests
from bs4 import BeautifulSoup
from io import StringIO
import os


class App:

    def __init__(self) -> None:
        st.set_page_config('Language detector app', layout='wide')
    
    def run(self) -> None:
        # text = BeautifulSoup(document.text, features='html.parser').get_text(strip=True, separator='\n')
        st.header('*LANGUAGE DETECTION APP*')
        st.write('### Choose text upload type')
        upload_type = st.selectbox('Upload type', options=['HTML files', 'URL'],
                                   key='upload_type')        
        raw_htmls: dict[str, str] = dict()
        if upload_type == 'HTML files':
            html_uploader = st.file_uploader(label='Upload HTML files here', type=('html', 'htm'),
                                             accept_multiple_files=True, key='html_uploader',
                                             help='Upload one or several *.htm or *.html files')
            if html_uploader:
                for html in html_uploader:
                    stringio = StringIO(html.getvalue().decode('utf-8'))
                    html_text = stringio.read()
                    html_path = os.path.realpath(os.path.join(os.path.dirname(__file__), html.name)).replace(os.sep, '/')
                    raw_htmls[html_path] = html_text
                    with open(f'./media/{html.name}', 'w', encoding='utf-8') as file:
                        file.write(stringio.read())
        elif upload_type == 'URL':
            url_input = st.text_area(label='Enter URLs line by line', key='url_input')
            if url_input:
                urls = url_input.split('\n')
                print(urls)
                for url in urls:
                    if not url:
                        continue
                    response = requests.get(url)
                    if response.status_code == 200:
                        html_text = response.text
                        html_path = os.path.realpath(
                            os.path.join(os.path.dirname(__file__),
                            f"media/{url.replace('.', '').replace('/', '').replace(':', '')}.html")
                        ).replace(os.sep, '/')
                        raw_htmls[html_path] = html_text
                        with open(html_path, 'w', encoding='utf-8') as file:
                            file.write(html_text)
        st.write('### Choose language detection type')
        detection_type = st.selectbox('Choose detection type', key='detection_type',
                                      options=['neural', 'alphabetic', 'ngram'])
        with st.expander('Language detection types explanation'):
            st.write('Neural - using ML model (https://huggingface.co/LocalDoc/language_detection);')
            st.write('N-gram - based on finding distances between text and 300 most popular 5-grams out of Russian and English texts;')
            st.write('Alphabetical - based on alphabet symbols amount. Language with most of its symbols wins.')
        detect_btn = st.button('## Recognize texts languages', key='detect_btn', type='primary')
        if detect_btn and raw_htmls:
            self._detect_languages(raw_htmls, detection_type)
    
    def _detect_languages(self, raw_htmls: dict[str, str], method: str) -> None:
        texts: dict[str, str] = dict()
        for path, html in raw_htmls.items():
            text = BeautifulSoup(html, features='html.parser').get_text(strip=True, separator='\n')
            texts[path] = text
        results: dict[str, str] = dict()
        for path, text in texts.items():
            if method == 'neural':
                language = neural_language(text)
            elif method == 'alphabetic':
                language = alphabetic_language(text)
            elif method == 'ngram':
                language = ngram_language(text)
            results[path] = language
        result_text = ''
        for path, language in results.items():
            with st.expander(path):
                st.write('Document hyperlink')
                st.write(f'<p><a href=file://localhost/{path}>{path}</a></p>', unsafe_allow_html=True)
                st.write(f'Document language: *{language}*')
                result_text += '\n'.join([f'Document path: {path}', f'Document language: {language}', f"{'-'*20}\n"])
        st.download_button('Download detection results', result_text, file_name='result.txt')


if __name__ == '__main__':
    app = App()
    app.run()

