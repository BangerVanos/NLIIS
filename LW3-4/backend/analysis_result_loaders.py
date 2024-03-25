import json
import os


class ResultLoader:

    @classmethod
    def load_syntactic_result(cls):
        try:
            with open(os.path.realpath(
                os.path.join(os.path.dirname(__file__),
                             'analysis_records/semantic_analysis.json')
            )) as file:
                result = json.load(file)
            return result
        except FileNotFoundError:
            return None

    @classmethod
    def load_semantic_syntactic_analysis(cls):
        try:
            with open(os.path.realpath(
                os.path.join(os.path.dirname(__file__),
                             'analysis_records/semantic_syntactic_analysis.json')
            )) as file:
                result = json.load(file)
            return result
        except FileNotFoundError:
            return None
