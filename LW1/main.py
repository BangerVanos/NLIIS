from nl_processor.pdf_reader import PDFReader
from nl_processor.vocabulary_creator import VocabularyCreator


if __name__ == '__main__':
    reader = PDFReader('test.pdf')
    text = reader.extract_text()    
    vocabulary_creator = VocabularyCreator(text)        
    print(vocabulary_creator.get_all_inflections())
    vocabulary_creator.save_inflections()   
