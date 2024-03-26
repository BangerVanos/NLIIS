import json
import os
from backend.analysis_result_loaders import ResultLoader


class ResultModifier:

    @classmethod
    def modify_syntactic_analysis(cls, modified_info):
        pass

    @classmethod
    def modify_semantic_analysis(cls, modified_info: dict[str, dict[str, list]]):
        old_result: dict[str, dict[str, list]] = ResultLoader.load_semantic_syntactic_analysis()
        old_result.update(modified_info)
        with open(os.path.realpath(os.path.join(
            os.path.dirname(__file__), 'analysis_records/semantic_syntactic_analysis.json'
        )), 'w') as file:
            json.dump(old_result, file, indent=4)
