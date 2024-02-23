import streamlit as st
from app.nl_processor.vocabulary_creator import VocabularyCreator, VocabularyRepository
from app.nl_processor.configs import NLConfigManager
import spacy


def modify_vocabulary_view():

    st.set_page_config(page_title='Modify and observe global vocabulary', layout='wide')

    st.title('Modify and observe global vocabulary')
    st.write('## Observe, modify existing or create new lemmas here ⬇️')

    options_button_columns = st.tabs(['Lookup vocabulary', 'Add new record with lemma inflections', 'Modify existing lemmas\' infomation'])
    with options_button_columns[0]:
        lookup_global_vocabulary()
    with options_button_columns[1]:
        create_new_lemma()
    with options_button_columns[2]:
        modify_existing_lemma()      


def lookup_global_vocabulary():
    load_filter_elements()
    st.session_state.global_vocabulary = VocabularyRepository.load_global_vocabulary()
    filter_vocabulary()
    with st.container(height=750, border=False):        
        st.write(f'## Global vocabulary size: {len(st.session_state.global_vocabulary)}')

        for lemma, info in dict(sorted(st.session_state.global_vocabulary.items(),
                                       key=lambda item: item[0].lower())).items():            
            st.text(f'- {(lemma.capitalize())}')
            for tag, inflections in info['inflections'].items():
                st.text(f'{', '.join(inflections)} - {spacy.explain(tag)}. '
                        f'May be part of {', '.join(info['sentence_part'])} in sentences.')


def load_filter_elements():
    with st.form(key='filter_form'):
        st.write('### Vocabulary filter parameters')
        # Filter parameters
        columns = st.columns(3)
        with columns[0]:
            st.write('Filter by lemma')
            lemma_filter = st.text_input(label='Input lemma here', key='lemma_filter',
                                         placeholder='Enter full or part of lemma here')
        
        with columns[1]:
            st.write('Filter by part of speech')
            pos_filter = st.selectbox(label='Choose part of speech', key='pos_filter', index=None,
                                      options=['Noun', 'Adjective', 'Adverb', 'Verb', 'Pronoun'])    
        with columns[2]:
            st.write('Filter by part of senetnce')
            part_filter = st.selectbox(label='Choose part of sentence', key='part_filter', index=None,
                                       options=['Simple subject', 'Complete subject', 'Compound subject',
                                                'Simple predicate', 'Complete predicate', 'Compound predicate',
                                                'Direct object', 'Indirect object', 'Complement', 'Modifier'])   
        st.form_submit_button(label='Filter vocabulary', help='Filter vocabulary by parameters',
                              on_click=filter_vocabulary, type='primary')


def filter_vocabulary():
    st.session_state.global_vocabulary = VocabularyRepository.filter_vocabulary(st.session_state.global_vocabulary,
                                                                                st.session_state.get('lemma_filter'),
                                                                                st.session_state.get('pos_filter'),
                                                                                st.session_state.get('part_filter'))


def create_new_lemma():
    st.session_state.new_lemma_config = {}
    configs = NLConfigManager()
    st.write('#### Input lemma below 🔻')
    lemma = st.text_input(label='Input lemma here', key='created_lemma')
    st.write('#### Choose part of speech of lemma below 🔻')
    part_of_speech = st.selectbox(label='Select lemma\'s part os speech',
                                  options=configs.pos_full_names.keys(),
                                  key='new_lemma_pos',
                                  index=None,
                                  format_func=format_short_pos_to_full
                                  )        
    if part_of_speech:
        st.write('#### Input inflections for this lemma below 🔻')        
        with st.container(height=250):
            possible_pos_tags = configs.tags_for_pos[part_of_speech]                                   
            for tag in possible_pos_tags:
                inflection_columns = st.columns([0.2, 0.8]) 
                with inflection_columns[0]:                
                    st.write(f'#### {format_possible_forms_for_pos(tag)}')
                with inflection_columns[1]:
                    st.text_input(label=f'Input inflection for {spacy.explain(tag)} here',
                                  key=f'{tag.lower()}_inflection',
                                  help='Input inflection according to form here.\n'
                                  'You can add several inflections by separating them with semicolon (;)')
        st.write('#### Select possible parts of sentence for this lemma below 🔻')
        parts_of_sentence = st.multiselect(label='Select possible parts of sentence for this lemma',
                                           key='parts_of_sentence', options=configs.parts_of_sentence,
                                           default=configs.possible_sentence_parts.get(part_of_speech,
                                                                                       'cannot clarify')
                                            )            
    submit_creation = st.button(label='Create new record',
                                help='Save all information about lemma in global vocabulary',                                 
                                )
    if submit_creation:
        submit_lemma_creation(lemma, part_of_speech, possible_pos_tags, parts_of_sentence)
        st.success(f'Succesfully created record for {lemma}')


def modify_existing_lemma():
    with st.form(key='modifying_filter'):
        st.write('#### Write lemma below to find and modify/delete it 🔻')
        lemma_filter = st.text_input(label='Input lemma here', key='modify_lemma_filter',
                                     placeholder='Enter full or part of lemma here')
        find_lemmas = st.form_submit_button(label='Find such lemmas',
                                            help='Click to find lemmas for change',
                                            )
    placeholder = st.container(height=750, border=False)          
    if find_lemmas:
        filtered_vocabulary: dict = VocabularyRepository.filter_vocabulary(
            VocabularyRepository.load_global_vocabulary(),
            lemma=lemma_filter.lower()
        )        
        with placeholder:
            if not filtered_vocabulary:
                st.write('### There is no such lemmas in this vocabulary')
            for lemma, info in filtered_vocabulary.items():
                columns = st.columns([0.2, 0.2, 0.4, 0.1, 0.1])
                with columns[0]:
                    st.write(f'##### {lemma}')
                with columns[1]:
                    st.write(f'##### {format_short_pos_to_full(info['pos'])}')
                with columns[3]:                             
                    st.button(label='Modify information', key=f'modify_{lemma}',
                              help=f'Modify information about `{lemma}` lemma',
                              on_click=lambda lemma=lemma: st.session_state.update({'modified_lemma': lemma}))
                    
                with columns[4]:
                    st.button(label='Delete lemma', key=f'delete_{lemma}',
                              help=f'Delete `{lemma}` from vocabulary',
                              on_click=lambda lemma=lemma: VocabularyRepository.modify_vocabulary([lemma], delete_only=True))
    if st.session_state.get('modified_lemma'):
        modify_existing_lemma_after_filter(st.session_state.get('modified_lemma'), placeholder)


def modify_existing_lemma_after_filter(lemma: str, placeholder):    
    configs = NLConfigManager()
    modified_lemma = VocabularyRepository.filter_vocabulary(
        VocabularyRepository.load_global_vocabulary(),
        lemma=lemma.lower()    
    )
    modified_lemma_info = modified_lemma[lemma]
    with placeholder:
        st.write(f'##### You are modifying `{lemma}` lemma')        
        modified_pos = st.selectbox(
            label='Modify part of speech',
            options=configs.pos_full_names.keys(),
            format_func=format_short_pos_to_full,
            index=list(configs.pos_full_names.keys()).index(modified_lemma_info['pos']),
            key=f'modify_{lemma.lower()}_pos'                      
        )        
        with st.container(height=400):
            possible_pos_tags = configs.tags_for_pos[modified_pos]                                   
            for tag in possible_pos_tags:
                inflection_columns = st.columns([0.2, 0.8]) 
                with inflection_columns[0]:                
                    st.write(f'#### {format_possible_forms_for_pos(tag)}')
                with inflection_columns[1]:
                    tag_inflections = modified_lemma_info['inflections'].get(tag)
                    st.text_input(label=f'Input inflection for {spacy.explain(tag)} here',
                                    key=f'modify_{tag.lower()}_inflection',
                                    help='Input inflection according to form here.\n'
                                    'You can add several inflections by separating them with semicolon (;)',
                                    value='; '.join(tag_inflections) if tag_inflections else None)
        parts_of_sentence = st.multiselect(label='Select possible parts of sentence for this lemma',
                                            key='modify_parts_of_sentence', options=configs.parts_of_sentence,
                                            default=modified_lemma_info.get('sentence_part',
                                                                            'cannot clarify')
                                            )
        submit_modifying = st.button(label=f'Modify {lemma} lemma',
                                        help='Save all information about lemma in global vocabulary',                                 
                                    )
        if submit_modifying:
            submit_lemma_modification(lemma, modified_pos, possible_pos_tags, parts_of_sentence)
            st.success(f'Succesfully modified information for {lemma}')
            st.session_state['modified_lemma'] = None



def format_short_pos_to_full(option):
    configs = NLConfigManager()
    return configs.pos_full_names.get(option)


def format_possible_forms_for_pos(option):    
    return spacy.explain(option).capitalize()


def submit_lemma_creation(lemma, pos, possible_tags, parts_of_sentence) -> None:
    lemma = lemma.lower() if not pos == 'PROPN' else lemma
    submitted_lemma = {
        lemma: {
            'pos': pos,
            'inflections': {
                tag: list(map(lambda item: item.strip(' '),
                              st.session_state.get(f'{tag.lower()}_inflection').split(';')))
                for tag in possible_tags
            },
            'sentence_part': parts_of_sentence,
            'creation_type': 'manual'
        }
    }
    VocabularyRepository.update_vocabulary(submitted_lemma)


def submit_lemma_modification(lemma, pos, possible_tags, parts_of_sentence) -> None:
    lemma = lemma.lower() if not pos == 'PROPN' else lemma
    submitted_lemma = {
        lemma: {
            'pos': pos,
            'inflections': {
                tag: list(map(lambda item: item.strip(' '),
                              st.session_state.get(f'modify_{tag.lower()}_inflection').split(';')))
                for tag in possible_tags
            },
            'sentence_part': parts_of_sentence,
            'creation_type': 'manual'
        }
    }
    VocabularyRepository.modify_vocabulary(submitted_lemma)
    


modify_vocabulary_view()
