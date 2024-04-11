import streamlit as st
from st_pages import show_pages, Page


class MainView:

    def __init__(self) -> None:
        st.set_page_config('Welcome', layout='wide')
    
    def run(self) -> None:
        show_pages([
            Page('app.py', name='Welcome page', icon='👋'),
            Page('app/frontend/load_files_view.py',
                 name='Load new info to DB',
                 icon='📂'),
            Page('app/frontend/chat_view.py',
                 name='Chat with Medicine Bot',
                 icon='💉')
        ])

        st.write('## Welcome!')

        st.info('Welcome in Medicine Chat-bot! We\'d like to provide you with '
                'some information on medicine. To start talking with Medicine '
                'Bot, visit Chat with Medicine Bot page. There is '
                'possibility for Bot to answer your questions '
                'based on information from medicine books '
                'you upload. To upload some of user\'s medicine '
                'books, visit Load new info to DB page. All of your questions '
                'are answered using TinyLlama-1.1B-Chat-v1.0 LLM')
        st.warning('There are some limits on using this app:\n'
                   '1. To use possibility of answering questions from '
                   'loaded books, >8GB of GPU RAM is needed.\n'
                   '2. User message editing do not cause Bot answer '
                   'regeneration.')

view = MainView()
view.run()
