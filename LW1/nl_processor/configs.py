import configparser
import os


class NLConfigManager:

    @staticmethod
    def spacy_core() -> str:
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 'configs.ini'))                          
        return config.get('SpacyConfig', 'LanguageCoreName')
