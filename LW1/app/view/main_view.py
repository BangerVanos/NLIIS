import streamlit as st
from ..nl_processor.pdf_reader import PDFReader
from ..nl_processor.vocabulary_creator import VocabularyCreator
import spacy


def main_view():
    st.set_page_config('Inflections App', layout='wide')

    st.title('Inflections app')
    st.write('## Load your PDF here ⬇️')
    pdf_file = st.file_uploader('Choose a PDF file', accept_multiple_files=False,
                                key='pdf_uploader', type='pdf')
    vocabulary_placeholder = st.empty()

    if pdf_file:
        text = PDFReader.extract_text_with_file(pdf_file)
        vocabulary = VocabularyCreator(text)
        inflections = vocabulary.get_all_inflections()        
        vocabulary.save_inflections()
        show_vocabulary(inflections, vocabulary_placeholder)


def show_vocabulary(vocabulary, placeholder) -> None:
    st.text(f'Vocabulary size: {len(vocabulary.keys())}')
    with placeholder.container(height=500):
        for unit, all_inflections in vocabulary.items():
            st.text(f'- {(unit.lemma.capitalize())}')
            for tag, inflections in all_inflections.items():
                st.text(f'{', '.join(inflections)} - {spacy.explain(tag)}')
