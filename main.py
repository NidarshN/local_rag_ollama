from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from helpers import config_logger
from dotenv import load_dotenv
from db import clear_database, populate_database, get_chromadb
import os
import argparse



def rag_query(query_text: str):
    PROMPT_TEMPLATE="""
        Answer the question based strongly on the following context:

        {context}

        ---

        Answer the question based on the above context: {question}
    """
    db = get_chromadb()
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = OllamaLLM(model=os.get_env("BASE_MODEL"))
    response_text = model.invoke(input=prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_results = f"Response: \n\n{response_text}\n\nSources: "
    print(formatted_results)
    for ind, source in enumerate(sources):
        print(f"{ind + 1}: {source}")
    print()
    return response_text

def main():
    load_dotenv()
    config_logger()
    parser = argparse.ArgumentParser(
        description="Local Retrieval Augmented Generation (RAG) using ollama"
    )
    parser.add_argument("--query-text", required=False, type=str, help="Query Text")
    parser.add_argument("--reset", action="store_true", required=False, help="Reset Database")
    parser.add_argument("--populate", action="store_true", required=False, help="Populate Database")
    parser.add_argument("--data-path", required=False, default=os.getenv("DATA_DIR"), type=str, help="Path to the diretory of the PDF documents to be processed. Default is './data/' directory")
    args = parser.parse_args()
    if(args.query_text):
        rag_query(args.query_text)
    elif(args.reset):
        clear_database()
    elif(args.populate):
        populate_database(data_dir=args.data_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
