import streamlit as st
from backend.modify_results import ResultModifier
from backend.analysis_result_loaders import ResultLoader
from nltk.tree import TreePrettyPrinter, Tree


class ModifyAnalysisResultsView:
    def __init__(self) -> None:
        st.set_page_config(page_title='Modify Analysis results',
                           layout='wide')
    
    def run(self) -> None:
        synt_tab, sem_tab = st.tabs(['Modify Syntactic analysis (LW 3)',
                                     'Modify Semantic-Syntactic Analysis (LW 4)'])
        with synt_tab:
            synt_view = ModifySyntacticAnalysisView()
            synt_view.run()
        
        with sem_tab:
            sem_view = ModifySemanticAnalysisView()
            sem_view.run()


class ModifySyntacticAnalysisView:
    
    def __init__(self) -> None:
        pass

    def run(self):
        old_result: dict[int, dict[str, str]] = ResultLoader.load_syntactic_analysis()
        with st.container(height=750, border=False):
            for ind, (_id, info) in enumerate(old_result.items(), 1):
                with st.expander(f'{ind}. {info['raw_sentence'].capitalize()}'):
                    sentence = info['raw_sentence'].capitalize()
                    st.write(f'Sentence: {sentence}')
                    st.write('Modify syntactic tree:')
                    feat_col, val_col = st.columns([1, 12])
                    with feat_col:
                        st.write('Penn treebank tree form:')
                    with val_col:
                        st.text_input(label='Modify',
                                      value=info['penn_treebank'],
                                      key=f'penn_{_id}',
                                      on_change=(lambda _id=_id, sentence=sentence: 
                                                 self._update_modified_info(_id, sentence)))
                    st.write('Preview syntactic tree:')
                    tree = Tree.fromstring(st.session_state.get(f'penn_{_id}'))
                    st.write(TreePrettyPrinter(tree).svg(nodecolor='black',
                                                         leafcolor='black',
                                                         funccolor='black'),
                             unsafe_allow_html=True)
        st.button(label='Save changes',
                  help='Save all changes',
                  key='save_syntactic_changes',
                  on_click=self._save_changes)
        
    
    def _update_modified_info(self, _id: int, sentence: str):
        if st.session_state.get('modified_syntactic_info') is None:
            st.session_state['modified_syntactic_info'] = {}
        penn_treebank = st.session_state.get(f'penn_{_id}')
        st.session_state['modified_syntactic_info'][_id] = {
            'raw_sentence': sentence,
            'penn_treebank': penn_treebank
        }

    def _save_changes(self):
        ResultModifier.modify_syntactic_analysis(
            st.session_state.get('modified_syntactic_info')
        )
        st.success('All changes have been saved!')
        st.session_state['modified_syntactic_info'] = {}


class ModifySemanticAnalysisView:
    
    def __init__(self) -> None:
        pass

    def run(self) -> None:
        old_result: dict[str, dict[str, list]] = ResultLoader.load_semantic_syntactic_analysis()        
        with st.container(height=750, border=False):
            for ind, (word, info) in enumerate(old_result.items(), 1):
                with st.expander(f'{ind}. {word.capitalize()}'):
                    st.write(f'Word - {word}')
                    st.write(f'Modify Semantic-syntactic analysis:')
                    for feature, values in info.items():
                        feat_col, val_col = st.columns([1, 12])
                        with feat_col:
                            st.write(f'{feature.capitalize()}:')
                        with val_col:
                            st.text_input(label='Modify',
                                          value=f'{'; '.join(values)}',
                                          key=f'{word.lower()}_{feature.lower()}',
                                          on_change=lambda word=word: self._update_modified_info(word))
        st.button(label='Save changes',
                  help='Save all changes',
                  key='save_semantic_changes',
                  on_click=self._save_changes)
    
    def _update_modified_info(self, word: str) -> None:
        if st.session_state.get('modified_semantic_info') is None:
            st.session_state['modified_semantic_info'] = {}
        examples = st.session_state.get(f'{word.lower()}_examples').split(';')
        synonyms = st.session_state.get(f'{word.lower()}_synonyms').split(';')
        antonyms = st.session_state.get(f'{word.lower()}_antonyms').split(';')
        hyponyms = st.session_state.get(f'{word.lower()}_hyponyms').split(';')
        hypernyms = st.session_state.get(f'{word.lower()}_hypernyms').split(';')
        st.session_state['modified_semantic_info'][word] = {
            'examples': list(map(lambda text: text.strip(), examples)),
            'synonyms': list(map(lambda text: text.strip().lower(), synonyms)),
            'antonyms': list(map(lambda text: text.strip().lower(), antonyms)),
            'hyponyms': list(map(lambda text: text.strip().lower(), hyponyms)),
            'hypernyms': list(map(lambda text: text.strip().lower(), hypernyms))
        }
        
    
    def _save_changes(self):
        ResultModifier.modify_semantic_analysis(st.session_state.get('modified_semantic_info'))
        st.success('All changes have been saved!')
        st.session_state['modified_semantic_info'] = {}


view = ModifyAnalysisResultsView()
view.run()
                            
