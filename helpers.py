from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_ollama import OllamaEmbeddings
import os
import logging
import shutil

logger = logging.getLogger(__name__)

def config_logger():
    """Function to configure the logger for the project
    
    Args:
    =====
    None
    
    Returns:
    ========
    None
    """
    LOG_DIR = os.getenv('LOG_DIR')
    LOG_FILE_PATH = os.path.join(LOG_DIR, os.getenv('LOG_FILE'))
    if(LOG_DIR == '' or (not os.path.exists(LOG_DIR))):
        logger.info(f'{LOG_DIR} does not exist')
        os.mkdir(LOG_DIR)
        logger.info(f'{LOG_DIR} created successfully!')
    logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO)


def get_embedding_function():
    """Function to get the embedding function for LLM
    
    Args:
    =====
    None
    
    Returns:
    ========
    Ollama Embedding Model : 
    """
    embedding = OllamaEmbeddings(model="nomic-embed-text")
    if not embedding:
        logger.info(f'Embedding Function failed to load!')
    return embedding

def load_documents(data_dir: str):
    """Function to load the documents from the datapath
    
    Args:
    =====
    None

    Returns:
    ========
    List[Documents] : Returns a list of documents present in the datapath
    """
    DATA_DIR = os.getenv('DATA_DIR')
    if(DATA_DIR == '' or (not os.path.exists(DATA_DIR))):
        logger.info(f'DATA: {DATA_DIR} does not exist')
        os.mkdir(DATA_DIR)
        logger.info(f'DATA: {DATA_DIR} created successfully!')
    if((data_dir is not None) and (data_dir != '') and (data_dir != DATA_DIR)):
        if(os.path.exists(data_dir)):
            pdf_files = [file for file in os.listdir(data_dir) if file.endswith('.pdf')]
            for file in pdf_files:
                shutil.copy(os.path.join(data_dir, file), os.path.join(DATA_DIR, file))
    document_loader = PyPDFDirectoryLoader(DATA_DIR)
    return document_loader.load()

def split_documents(documents: list[Document]):
    """Function to split the document text into chunks
    
    Args:
    =====
    List[Documents] : Returns a list of documents present in the datapath

    Returns:
    ========
    List[Documents] : Returns a list of documents present in the datapath
    """
    test_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return test_splitter.split_documents(documents)

