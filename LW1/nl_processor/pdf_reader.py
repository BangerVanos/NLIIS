import PyPDF2 as pdf


class PDFReader:
    """Class for extracting text from PDF document"""

    def __init__(self, path: str):
        self._path = path

    def extract_text(self) -> str:
        """Returns all text form PDF document"""
        with open(self._path, 'rb') as file:
            reader = pdf.PdfReader(file)
            return '\n'.join([page.extract_text() for page in reader.pages])
