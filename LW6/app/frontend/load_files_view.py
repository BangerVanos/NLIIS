import streamlit as st
import tempfile
from app.backend.chroma_db_handler import ChromaDBUpdater
import os


class LoadFilesView:

    def __init__(self) -> None:
        st.set_page_config(page_title='Load new files to DB',
                           layout='wide')
    
    def run(self) -> None:
        st.info('### Load PDF files with medicine texts here')
        uploaded_files = st.file_uploader(label='Upload PDF files',
                                          type='pdf',
                                          accept_multiple_files=True)
        for file in uploaded_files:
            try:
                with tempfile.NamedTemporaryFile(delete=False) as f:
                    f.write(file.read())
                    f.flush()
                    ChromaDBUpdater.upload_file(f.name)
                os.unlink(f.name)
            except Exception as err:
                st.error(f'Error while uploading file {f.name}: {err}!')
            else:
                st.write(f'File {f.name} succesfully uploaded!')        


view = LoadFilesView()
view.run()
