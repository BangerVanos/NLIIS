import streamlit as st
from app.backend.chat_history import ChatHistory
from app.backend.chat_handler import QueryHandler


class ChatView:

    def __init__(self) -> None:
        st.set_page_config(page_title='Discuss',
                           layout='wide')
    
    def run(self) -> None:
        with st.sidebar:
            st.checkbox('Use information from loaded docs?',
                        key='use_docs',
                        help='If not checked, bot will rely on its own knowledge')
        chat_history = ChatHistory.load_history()
        query_func = {
            True: QueryHandler().handle_query,
            False: QueryHandler().handle_raw_query
        }
        with st.container(height=750):
            for ind, message in enumerate(chat_history):
                with st.chat_message(name=message['role']):                                        
                    if message['role'] == 'user':
                        text_col, edit_col = st.columns([15, 1])
                        with text_col:
                            st.write(message['content'])
                        with edit_col:
                            edit_btn = st.button('Edit', key=f'edit_{ind}')
                        if edit_btn:
                            st.divider()
                            text_col, save_col, cancel_col = st.columns([15, 2, 2])
                            with text_col:
                                new_input = st.text_input(label='Enter new input',
                                                          key=f'edit_input_{ind}',
                                                          value=message['content'],
                                                          placeholder='Rewrite message...')
                            with save_col:                                
                                st.button('Save', key=f'save_{ind}',
                                          on_click=(lambda ind=ind:
                                                    ChatHistory.edit_user_input(ind,
                                                                                st.session_state
                                                                                .get(f'edit_input_{ind}')
                                                                                )
                                                    )
                                          )
                            with cancel_col:
                                st.button('Cancel', key=f'cancel_{ind}')
                    else:
                        st.write(message['content'])
        if prompt := st.chat_input('Say something here'):
            new_messages = [{
                'role': 'user',
                'content': prompt
            }]
            answer = (query_func[st.session_state.get('use_docs', False)](prompt))
            new_messages.append({
                'role': 'assistant',
                'content': answer
            })
            ChatHistory.update_history(new_messages)
            st.rerun()


view = ChatView()
view.run()
