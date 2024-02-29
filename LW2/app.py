import streamlit as st
from st_pages import Page, show_pages


class WelcomePage:

    def __init__(self) -> None:
        st.set_page_config(page_title='Welcome page',page_icon='🤗', layout='wide')
        self._page_list = [
            Page('app.py', name='Welcome page', icon='🤗'),
            Page('app/frontend/main_view.py', name='Main page', icon='🧾'),
            Page('app/frontend/modify_word_stats_view.py', name='Modify', icon='🛠️'),
            Page('app/frontend/update_text_corpus_view.py',
                 name='Upload new texts to corpus', icon='📝')
        ]
    

    def run(self):
        show_pages(self._page_list)


welcome_page = WelcomePage()
welcome_page.run()
