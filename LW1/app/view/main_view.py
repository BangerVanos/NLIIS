import streamlit as st
from app.nl_processor.pdf_reader import PDFReader
from app.nl_processor.vocabulary_creator import VocabularyCreator
import spacy
import json
import os


def main_view():
    st.set_page_config('Inflections App', layout='wide')

    with st.sidebar:                
        st.warning('Need help? Go to *Welcome page* for beginner tutorial')
        

    st.title('Inflections app')
    st.write('## Load your PDF here ⬇️')
    pdf_file = st.file_uploader('Choose a PDF file', accept_multiple_files=False,
                                key='pdf_uploader', type='pdf')    

    if pdf_file:
        text = PDFReader.extract_text_with_file(pdf_file)
        vocabulary = VocabularyCreator(text)                
        vocabulary.save_inflections(global_vocabulary=True)
        show_vocabulary(text)


def show_vocabulary(text: str) -> None:
    st.write('### Your text ⬇️')
    with st.empty().container(height=250):
        st.text(text)
    
    with open(os.path.join(os.path.dirname(__file__), '../vocabularies/vocabulary.json')) as file:
        st.session_state.vocabulary = json.load(file)
        filter_vocabulary()                   
    
    load_filter_elements()    
    st.write(f'### Vocabulary size: {len(st.session_state.get('vocabulary').keys())}')       

    with st.empty().container(height=500):
        for lemma, info in st.session_state.get('vocabulary').items():            
            st.text(f'- {(lemma.capitalize())}')
            for tag, inflections in info['inflections'].items():
                st.text(f'{', '.join(inflections)} - {spacy.explain(tag)}. '
                        f'May be part of {', '.join(info['sentence_part'])} in sentences.')


def load_filter_elements():
    with st.form(key='filter_form'):
        st.write('### Vocabulary filter parameters')
        # Filter parameters
        columns = st.columns(3)
        with columns[0]:
            st.write('Filter by lemma')
            lemma_filter = st.text_input(label='Input lemma here', key='lemma_filter',
                                         placeholder='Enter full or part of lemma here')
        
        with columns[1]:
            st.write('Filter by part of speech')
            pos_filter = st.selectbox(label='Choose part of speech', key='pos_filter', index=None,
                                      options=['Noun', 'Adjective', 'Adverb', 'Verb', 'Pronoun'])    
        with columns[2]:
            st.write('Filter by part of senetnce')
            part_filter = st.selectbox(label='Choose part of sentence', key='part_filter', index=None,
                                       options=['Simple subject', 'Complete subject', 'Compound subject',
                                                'Simple predicate', 'Complete predicate', 'Compound predicate',
                                                'Direct object', 'Indirect object', 'Complement', 'Modifier'])   
        st.form_submit_button(label='Filter vocabulary', help='Filter vocabulary by parameters',
                              on_click=filter_vocabulary, type='primary')


def filter_vocabulary():    
    if st.session_state.get('lemma_filter'):
        st.session_state.vocabulary = dict(filter(lambda pair: st.session_state.lemma_filter.lower()
                                           in pair[0].lower(), st.session_state.vocabulary.items()))        
    if st.session_state.get('pos_filter'):            
        st.session_state.vocabulary = dict(filter(lambda pair: 
                                           st.session_state.pos_filter.lower().startswith(pair[1]['pos'].lower()),                                                                        
                                           st.session_state.vocabulary.items()))        
    if st.session_state.get('part_filter'):
        st.session_state.vocabulary = dict(filter(lambda pair: st.session_state.part_filter.lower()
                                           in pair[1]['sentence_part'], st.session_state.vocabulary.items()))


main_view()        
