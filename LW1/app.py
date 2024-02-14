import st_pages as pg
import streamlit as st


pg.show_pages(
    [
        pg.Page('app.py', 'Welcome page', icon='🌏'),
        pg.Page('app/view/main_view.py', name='Main page', icon='🖥️')
    ]
)

st.set_page_config(page_title='Welcome!', layout='wide')

st.write('## Welcome to inflections analyzer app!')
st.info('First time using app? Here is small tutorial on how to use it:\n'
        '1. Go to *Main page* page to use this app;\n'
        '2. After choosing *Main page*, upload your PDF with text to analyze:\n'
        '3. Once PDF file is uploaded, you will see blocks containing text from PDF file and '
        'vocabulary with lemmas, their inflections and inflections`s possible part of sentence;\n'
        '4. If text is uploaded, users will have possibility to filter text\'s vocabulary by '
        'lemmas, parts of speech and parts of sentence;\n'
        '5. After setting filters\' conditions, user may push *Filter vocabulary* button to see '
        'filtered vocabulary;\n'
        '6. Users may want to see unfiltered vocabulary. To do this, all filters should be cleared and '
        '*Filter vocabulary* button pressed again.')
st.warning('There are some limitations on using this app:\n'
           '1. Only PDF files are supported to upload;\n'
           '2. Only English language texts are supported.')
