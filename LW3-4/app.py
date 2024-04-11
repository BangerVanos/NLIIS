import streamlit as st
from st_pages import Page, show_pages
from backend.syntactic_analysis import SyntacticAnalysis


class WelcomeView:

    def __init__(self) -> None:
        st.set_page_config('Welcome page', layout='wide')
        show_pages(
            [
                Page('app.py', 'Welcome', '🌐'),
                Page('frontend/file_load_view.py', 'Load PDF', '⏪'),
                Page('frontend/analysis_view.py', 'Observe Analysis', '🔍'),
                Page('frontend/modify_results_view.py', 'Modify Analysis Results', '🛠')
            ]
        )
    
    def run(self) -> None:
        st.write('## Welcome!')
        st.info('This NLP app can provide its users with syntactic and semantic analysis.\n'
                'To perform analysis users should visit Load PDF page first and upload their '
                'PDF files containing English language texts.'
                'After that they should wait for some time until text from this file appears '
                'on screen. That means analysis have been performed.\n'
                'Nextly, users can visit Observe Analysis page to see syntactic and '
                'semantic analysis of their texts. To change the type of observed '
                'analysis users can switch between tabs.\n'
                'There is possibility for users to correct analysis results. To do this '
                'they could visit Modify Analysis Results page. After correcting analysis '
                'results users should press Save all changes button to save their corrections. '
                'Otherwise, corrections would not be saved.')
        st.warning('1. Only English language texts are supported.\n'
                   '2. Only PDF files are possible to upload.\n'
                   '3. Penn Treebank tag system is used in this app. For more information '
                   'about this system visit: https://www.researchgate.net/figure/'
                   'The-Penn-Treebank-POS-tagset_tbl1_220017637\n'
                   '4. Penn Treebank notation is used for string representation of sentence '
                   'syntactic tree. For more information visit: https://catalog.ldc.upenn.edu/'
                   'docs/LDC95T7/cl93.html')


view = WelcomeView()
view.run()
