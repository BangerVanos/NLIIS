from nl_processor.pdf_reader import PDFReader
from nl_processor.vocabulary_creator import LexemeCreator


if __name__ == '__main__':
    reader = PDFReader('test.pdf')
    text = reader.extract_text
    lexeme_creator = LexemeCreator(text)
    print(lexeme_creator.get_lemmas())
