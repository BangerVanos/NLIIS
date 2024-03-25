import streamlit as st
from backend.file_load import PDFReader
from backend.words_finder import WordsFinder
from backend.semantic_syntactic_analysis import SemanticSyntacticAnalysis


class FileLoadView:

    def __init__(self) -> None:
        st.set_page_config(page_title='Load file here',
                           layout='wide')

    def run(self) -> None:
        st.info('## You can upload your file with text here')
        file = st.file_uploader(label='Upload your PDF file here',
                                type='pdf',
                                accept_multiple_files=False,
                                key='pdf_file')
        if file:
            st.session_state['text_loaded'] = True
            st.write('## Here is your text')
            text = PDFReader.extract_text_with_file(file)
            st.session_state['text'] = text

            self._make_analysis(text)

            with st.container(height=500, border=True):                
                st.write(text)
            st.write('## Now you can move to Analysis page to '
                     'perform different analysis types')
        else:
            st.session_state['text_loaded'] = False            

    def _make_analysis(self, text):
        word_finder = WordsFinder()
        words = word_finder.find_words(text)
        SemanticSyntacticAnalysis.semantic_syntactic_analysis(words, save=True)  


view = FileLoadView()
view.run()
