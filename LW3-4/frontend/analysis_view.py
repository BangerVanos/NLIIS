import streamlit as st
from backend.analysis_result_loaders import ResultLoader


class AnalysisView:
    def __init__(self) -> None:
        st.set_page_config(page_title='Analysis',
                           layout='wide')
    
    def run(self) -> None:
        synt_tab, sem_tab = st.tabs(['Syntactic analysis (LW 3)',
                                     'Semantic-Syntactic Analysis (LW 4)'])
        with synt_tab:
            synt_view = SyntacticAnalysisView()
            synt_view.run()
        
        with sem_tab:
            sem_view = SemanticSyntacticAnalysisView()
            sem_view.run()


class SyntacticAnalysisView:
    
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        pass


class SemanticSyntacticAnalysisView:

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        result = ResultLoader.load_semantic_syntactic_analysis()
        st.write(result)


view = AnalysisView()
view.run()
