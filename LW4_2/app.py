import streamlit as st
from translator import Translator


st.set_page_config('Translation page', layout='wide')
if not 'translator' in st.session_state:
    st.session_state['translator'] = Translator()
translator: Translator = st.session_state['translator']


def translation_view() -> None:
    st.write('### Translate your text here')
    original_col, translation_col = st.columns([3, 7])
    translation_statistics = None
    translation_statistics_to_save: str | None = None
    with original_col:
        st.write('Original text')
        original_text = st.text_area(label='Original text (English)', height=300)
        translate_btn = st.button(label='Translate', key='translate_btn')
        if translate_btn:
            translation_statistics = translator.translate(original_text)
            translation_statistics_to_save = translator.parse_statistics(translation_statistics)
    with translation_col:
        st.write('Translation statistics')
        if translation_statistics:
            with st.empty().container(height=300, border=True):
                st.text(translation_statistics_to_save)
            save_btn = st.download_button(label='Save data', data=translation_statistics_to_save,
                                          file_name='result.txt', key='save_btn',
                                          help='Save translation statistics to data')


def vocabulary_view() -> None:
    print('dkkbnrk')
    st.write('### Current vocabulary')
    with st.container(height=500, border=None):
        st.write(translator.parse_vocabulary())
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
        st.session_state['translator'] = translator


page = st.navigation([
    st.Page(translation_view, title='Translate text'),
    st.Page("vocabulary_page.py", title='Vocabulary')
])
page.run()
