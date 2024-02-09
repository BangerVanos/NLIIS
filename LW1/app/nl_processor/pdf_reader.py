import PyPDF2 as pdf


class PDFReader:
    """Class for extracting text from PDF document"""

    
    @classmethod
    def extract_text_with_path(cls, path) -> str:
        """Returns all text form PDF document"""
        with open(path, 'rb') as file:            
            return cls.extract_text_with_file(file)
    
    @classmethod
    def extract_text_with_file(cls, file):
        reader = pdf.PdfReader(file)
        return '\n'.join([page.extract_text() for page in reader.pages])
