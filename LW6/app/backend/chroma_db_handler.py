from langchain.document_loaders import TextLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import os


class EmbeddingsCreator:

    @classmethod
    def create_embeddings(cls):
        model_name = os.path.realpath(os.path.join(
            os.path.dirname(__file__),
            'sentence-transformers/all-mpnet-base-v2'
        ))
        model_kwargs = {
            'device': 'cuda'
        }
        embeddings = HuggingFaceEmbeddings(model_name=model_name,
                                           model_kwargs=model_kwargs)
        return embeddings


class ChromaDBUpdater:

    @classmethod
    def upload_file(cls, file_path: str) -> None:
        """Can only update docs DB with one
        doc at time"""
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                       chunk_overlap=20)
        all_splits = text_splitter.split_documents(documents)

        
        vector_db_path = os.path.realpath(os.path.join(
            os.path.dirname(__file__),
            'chroma_db'
        ))
        
        vectordb = Chroma.from_documents(documents=all_splits,
                                         embedding=EmbeddingsCreator.create_embeddings(),
                                         persist_directory=vector_db_path)


class ChromaDBRetriever:

    @classmethod
    def get_retriever(cls):

        vector_db_path = os.path.realpath(os.path.join(
            os.path.dirname(__file__),
            'chroma_db'
        ))        
        vector_db = Chroma(persist_directory=vector_db_path,
                           embedding_function=EmbeddingsCreator.create_embeddings())
        return vector_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.5, 'k': 2}
        )

