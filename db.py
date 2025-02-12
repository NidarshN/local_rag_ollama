from langchain_chroma import Chroma
from langchain.schema.document import Document
from helpers import get_embedding_function, load_documents, split_documents
import os
import shutil
import logging


logger = logging.getLogger(__name__)

def get_chromadb():
    """Function to get the Chroma Database Client
    
    Args:
    =====
    None
    
    Returns:
    ========
    db (Chroma Database Client) : Object of Chroma Database Client
    """
    DB_DIR = os.getenv('DB_DIR')
    if(DB_DIR == '' or (not os.path.exists(DB_DIR))):
        logger.info(f'DB: {DB_DIR} does not exist')
        os.mkdir(DB_DIR)
        logger.info(f'DB: {DB_DIR} created successfully!')
    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=get_embedding_function()
    )
    return db

def add_rag_documents(documents: list[Document]):
    """Function to add documents to the Chroma Database
    
    Args:
    =====
    documents (list[Document]) : List of Documents to be added to the database
    
    Returns:
    ========
    None
    """
    db = get_chromadb()

    doc_chunks_with_ids = calculate_doc_chunks(documents)

    existing_docs = db.get(include=[])
    existing_ids = set(existing_docs["ids"])
    logger.info(f"Documents Count in the database: {len(existing_ids)}")

    new_doc_chunks = []
    for doc_chunk in doc_chunks_with_ids:
        if(doc_chunk.metadata["id"] not in existing_ids):
            new_doc_chunks.append(doc_chunk)
    
    if(len(new_doc_chunks)):
        new_doc_chunk_ids = [doc_chunk.metadata["id"] for doc_chunk in new_doc_chunks]
        db.add_documents(new_doc_chunks, ids=new_doc_chunk_ids)
        logger.info(f"Added {new_doc_chunks} new documents to the database!")
        print("Documents added to the database!")
    else:
        logger.info(f"No neew documents were added to the database!")


def calculate_doc_chunks(documents: list[Document]):
    """Function to calculate and assign chunks id for documents
    
    Args:
    =====
    documents (list[Document]) : List of Documents to be stored in the database
    
    Returns:
    ========
    documents (list[Document]) : List of Documents with chunk ids to be stored in the database
    """
    last_page_id = None
    curr_chunk_idx = 0

    for document in documents:
        doc_src = document.metadata.get('source')
        page = document.metadata.get('page')
        curr_page_id = f"{doc_src}:{page}"

        curr_chunk_idx = curr_chunk_idx + 1 if (curr_page_id == last_page_id) else 0

        chunk_id = f"{curr_page_id}:{curr_chunk_idx}"
        last_page_id = curr_page_id 

        document.metadata["id"] = chunk_id
    return documents

def clear_database():
    """Function to purge the database
    
    Args:
    =====
    None
    
    Returns:
    ========
    None
    """
    DB_DIR = os.getenv('DB_DIR')
    if(DB_DIR != '' and os.path.exists(DB_DIR)):
        shutil.rmtree(DB_DIR)
        logger.info("Purged Database successfully!")

def populate_database(data_dir: str):
    """Function to populate the database with the documents present in the DATA_DIR
    
    Args:
    =====
    None

    Returns:
    ========
    None
    """
    documents = load_documents(data_dir)
    documents = split_documents(documents)
    add_rag_documents(documents)
    logger.info("Database populated successfully!")