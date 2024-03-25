from nltk.corpus import wordnet as wn
import json
import os


class SemanticSyntacticAnalysis:
    
    @classmethod
    def semantic_syntactic_analysis(cls, words: list[str], save: bool = True):

        result = {}

        for word in range(len(words)):
            words[word] = words[word].lower()

        for word in words:
            examples = []
            synonyms = []
            antonyms = []
            hyponyms = []
            hypernyms = []
            syn = wn.synsets(word)

            if len(syn) > 0:
                if len(syn[0].examples()) > 0:
                    examples = syn[0].examples()

                for synset in syn:
                    for lemma in synset.lemmas():
                        synonyms.append(lemma.name())
                        if lemma.antonyms():
                            antonyms.append(lemma.antonyms()[0].name())

                    for hyp in synset.hyponyms():
                        hyponyms.append(hyp.name()[0:-5])

                    for hyp in synset.hypernyms():
                        hypernyms.append(hyp.name()[0:-5])

            result[word] = {
                'examples': examples,
                'synonyms': list(set(synonyms)),
                'antonyms': list(set(antonyms)),
                'hyponyms': hyponyms,
                'hypernyms': hypernyms                
            }
        
        if save:
            cls._save_to_json(result)

        return result
    
    @classmethod
    def _save_to_json(cls, result: dict) -> None:
        with open(os.path.realpath(os.path.join(
            os.path.dirname(__file__), 'analysis_records/semantic_syntactic_analysis.json'
        )), 'w') as file:
            json.dump(result, file, indent=4)
