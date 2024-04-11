from threading import Lock
import os
from transformers import BitsAndBytesConfig
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline
from torch import bfloat16
from langchain import HuggingFacePipeline
from langchain.chains import LLMChain,ConversationalRetrievalChain, RetrievalQA
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFacePipeline
from langchain.document_loaders import TextLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from app.backend.chroma_db_handler import ChromaDBRetriever


class LLMSingletonMeta(type):

    _instances = {}
    _lock: Lock = Lock()

    def __call__(self, *args, **kwargs):
        with self._lock:
            if self not in self._instances:
                instance = super().__call__(*args, **kwargs)
                self._instances[self] = instance
        return self._instances[self]


class LLM(metaclass=LLMSingletonMeta):

    def __init__(self) -> None:
        self._model_id = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                'llm/TinyLlama-1.1B-Chat-v1.0'
            )
        )

        self._bnb_config = BitsAndBytesConfig(load_in_4bit=True,
                                              bnb_4bit_quant_type='nf4',
                                              bnb_4bit_use_double_quant=True,
                                              bnb_4bit_compute_dtype=bfloat16
                                              )

        self._tokenizer = AutoTokenizer.from_pretrained(self._model_id)
        self._model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=self._model_id,
            quantization_config=self._bnb_config,
            device_map='auto',
            torch_dtype='auto'
        )
        self._model_config = AutoConfig.from_pretrained(self._model_id)

        self._pipeline = pipeline(
            task='text-generation',
            model=self._model,
            tokenizer=self._tokenizer,
            config=self._model_config,            
            max_new_tokens=2000,
            trust_remote_code=True,
            device_map='auto',
            torch_dtype='auto',            
        )

        self._llm = HuggingFacePipeline(pipeline=self._pipeline)
    
    @property
    def tokenizer(self):
        return self._tokenizer
    
    @property
    def llm(self):
        return self._llm
    
    @property
    def model(self):
        return self._model
                                              

class QueryHandlerSingletonMeta(type):

    _instances = {}
    _lock: Lock = Lock()

    def __call__(self, *args, **kwargs):
        with self._lock:
            if self not in self._instances:
                instance = super().__call__(*args, **kwargs)
                self._instances[self] = instance
        return self._instances[self]


class QueryHandler(metaclass=QueryHandlerSingletonMeta):

    def __init__(self) -> None:
        self._question_generator = LLMChain(
            llm=LLM().llm,
            prompt=CONDENSE_QUESTION_PROMPT
        )
        self._doc_chain = load_qa_chain(llm=LLM().llm,
                                        chain_type='stuff')
        self._chain = ConversationalRetrievalChain(
            retriever=ChromaDBRetriever.get_retriever(),
            question_generator=self._question_generator,
            combine_docs_chain=self._doc_chain
        )
    
    def handle_query(self, query: str) -> str:
        doc_search_result = self._chain(
            {"question": query, "chat_history": []}
        )
        prompt = doc_search_result['answer']        

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        tokenizer = LLM().tokenizer
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        print(text)
        model_inputs = tokenizer([text], return_tensors="pt").to('cuda')

        model = LLM().model

        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids
            in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        print(len(response.split(' ')))        
        return(response)

    def handle_raw_query(self, query: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
        tokenizer = LLM().tokenizer
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to('cuda')
        generated_ids = LLM().model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return(response)
