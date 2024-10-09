import streamlit as st
from translator import Translator


translator: Translator | None = st.session_state.get('translator')


def vocabulary_view() -> None:
    if translator is None:
        st.error('Load "Translation text" text to get access to vocabulary!')
        return
    st.write('### Current vocabulary')
    with st.container(height=500, border=None):
        for pair in translator.parse_vocabulary().split('\n'):
            st.write(pair)
    st.write('### Update vocabulary')
    user_vocabulary = st.text_area(label='Update vocabulary',
                                   help='Update vocabulary by writing lines like "word - translation"')
    with st.expander('User vocabulary syntax'):
        st.write('Update vocabulary by writing lines like "word - translation"')
        st.write('For example, you can write line: "they - они"')
    update_btn = st.button(label='Update vocabulary', key='update_btn')
    if update_btn:
        pairs = user_vocabulary.split('\n')
        pairs = [pair for pair in pairs if pair != '']
        new_words = {}
        for pair in pairs:
            split = pair.split('-')
            new_words[split[0].strip().lower()] = split[1].strip().lower()
        translator.update_vocabulary(new_words)


vocabulary_view()
