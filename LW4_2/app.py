import streamlit as st
from translator import Translator
from nltk.tree import Tree, TreePrettyPrinter
import base64


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
    if translation_statistics:
        with translation_col:
            st.write('Translation statistics')        
            with st.empty().container(height=300, border=True):
                st.text(translation_statistics_to_save)
            save_btn = st.download_button(label='Save data', data=translation_statistics_to_save,
                                          file_name='result.txt', key='save_btn',
                                          help='Save translation statistics to data')
        for ind, sent_stat in enumerate(translation_statistics['statistics'], 1):
            with st.expander(label=f'{ind}. {sent_stat["original"]}'):
                st.write(f'Original text: {sent_stat["original"]}')
                st.write(f'Translation: {sent_stat["translation"]}')
                st.write(f'Original text word amount: {sent_stat["original_words_amount"]}')
                st.write(f'Translation words amount: {sent_stat["translated_words_amount"]}')
                st.write('Syntax tree:')
                tree = Tree.fromstring(sent_stat['syntax_tree'])
                svg = TreePrettyPrinter(tree).svg()
                b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
                html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
                st.write(html, unsafe_allow_html=True)


page = st.navigation([
    st.Page(translation_view, title='Translate text'),
    st.Page("vocabulary_page.py", title='Vocabulary')
])
page.run()
