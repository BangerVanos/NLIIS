import streamlit as st
import pandas as pd
import os
from app.backend.text_ectractors import TextEctractor


class MainView:

    def __init__(self) -> None:
        pass
    
    def run(self):
        st.set_page_config(page_title='Main view', layout='wide')
        text_upload_selector = st.selectbox(label='Choose way of text input',
                                            options=['Manual', 'Via file'],
                                            index=0,
                                            key='text_input_option')
        if st.session_state.get('text_input_option') == 'Manual':
            self._render_extrude_text_via_text_input()
        elif st.session_state.get('text_input_option') == 'Via file':
            self._render_extrude_text_via_file()
        self._render_submit_text_upload_button()   

    def _render_extrude_text_via_text_input(self):
        text_area = st.text_area(label='Input text to analyze here',
                                 placeholder='Input text for analysis here.\n'
                                             'For example, \'Diarea\'',
                                 key='text_area_input_field'
                                )

    def _render_extrude_text_via_file(self):
        file_input = st.file_uploader(label='Upload your file with text here',
                                      type=['pdf', 'docx', 'txt', 'rtf', 'doc'],
                                      key='file_input_field')

    def _render_submit_text_upload_button(self):
        submit_button = st.button(label='Upload text', key='upload_text_btn',
                                  help='Upload your text to analysis',
                                  on_click=self._upload_text
                                  )
    
    def _upload_text(self):
        if st.session_state.get('text_input_option') == 'Manual':
            if st.session_state.get('text_area_input_field'):
                pass
            else:
                st.error('Write something into text field first!')
        elif st.session_state.get('text_input_option') == 'Via file':
            if file := st.session_state.get('file_input_field'):                                                 
                st.write(TextEctractor.extract_text(file, file.type))
            else:
                st.error('Upload your file first!')


view = MainView()
view.run()
