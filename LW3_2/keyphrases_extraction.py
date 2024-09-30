from rake_nltk import Rake


def keyphrases_extraction(text: str, language: str = 'russian', top_n: int = 10) -> list[str]:
    rake = Rake(language=language, max_length=2,
                include_repeated_phrases=True)
    rake.extract_keywords_from_text(text)
    keyphrases = rake.get_ranked_phrases()[:top_n]    
    return keyphrases
