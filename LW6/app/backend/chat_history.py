import json
import os


class ChatHistory:

    @classmethod
    def load_history(cls) -> list[dict[str, str]]:
        with open(os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                'chat_history/chat_history.json'
            )
        )) as file:
            try:
                history: list[dict[str, str]] = json.load(file)
            except json.JSONDecodeError:
                history = []
        return history
    
    @classmethod
    def update_history(cls, messages: list[dict[str, str]]):
        history = cls.load_history()        
        history.extend(messages)
        with open(os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                'chat_history/chat_history.json'
            )
        ), 'w') as file:            
            json.dump(history, file, indent=4)
    
    @classmethod
    def edit_user_input(cls, message_ind: int,
                        new_input: str):
        history = cls.load_history()
        history[message_ind]['content'] = new_input
        with open(os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                'chat_history/chat_history.json'
            )
        ), 'w') as file:            
            json.dump(history, file, indent=4)
