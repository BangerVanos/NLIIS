import streamlit as st
from st_pages import Page, show_pages


class WelcomeView:

    def __init__(self) -> None:
        show_pages(
            [
                Page('app.py', 'Welcome'),
                Page('frontend/file_load_view.py', 'Load PDF'),
                Page('frontend/analysis_view.py', 'Observe Analysis'),
                Page('frontend/modify_results_view.py', 'Modify analysis results')
            ]
        )
    
    def run(self) -> None:
        pass


view = WelcomeView()
view.run()
