import configparser
import os


class NLConfigManager:

    @staticmethod
    def spacy_core() -> str:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.getcwd(), 'configs.ini'))                
        return config.get('SpacyConfig', 'LanguageCoreName')
