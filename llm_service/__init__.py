"""
Description:    The app is used to search for the relevant documents of the respective system and send them to the LLM.
                The response from the LLM is then awaited and the result is sent back.
Author:         Timm Straub
Version:        0.1
Created at:     2025/08/04
Last change:    2025/08/04
"""

import re
import time
from typing import Literal

from fastapi import FastAPI
from langchain_community.vectorstores import FAISS

from connections.mailserver_connection import EmailService
from entities.embedding import multi_lingual_embedder
from entities.ollama_entities import Llama3, Phi4_friendly
from entities.request_entities import LLMRequest, PageRequest, LLMRequestPapers
from services.images import get_erp_images, image_from_path
from services.indices.generate_confluence_index import get_confluence_vec_store, ConfluenceVecStoreSingleton
from services.indices.generate_paper_index import get_paper_vec_store
from services.papers.generate_image_descriptions import generate_paper_image_descriptions
from utils import bin_images_to_text
from utils.constants import CONFLUENCE_EXAMPLE_QUERY, document_retrieval_prompt, paper_prompt, email_prompt
from utils.logging_config import logger, exception_handling, log_report_time, \
    log_llm_report_time
from utils.paper_utils import retrieve_docs_from_erp_handbook, erp_handbook_index, erp_handbook_index_path
from utils.paths import FAISS_CONFLUENCE_TEXTS_IDX_FOLDER

app = FastAPI()


@app.get("/")
async def root(test: bool = False) -> dict:
    if test:
        return {"message": "Test"}
    return {"message": "Root"}


@app.get("/gen_confluence_index")
@log_report_time
@exception_handling
def gen_confluence_index(confluence_index_path: str = FAISS_CONFLUENCE_TEXTS_IDX_FOLDER, new_index: bool = True):
    ConfluenceVecStoreSingleton.get_instance(confluence_index_path, new_index)
    return {"Result": "Successful"}


@app.get("/get_confluence_docs")
@log_report_time
@exception_handling
def confluence_doc_retriever(input: str = CONFLUENCE_EXAMPLE_QUERY,
                             confluence_index_path: str = FAISS_CONFLUENCE_TEXTS_IDX_FOLDER,
                             k: int = 10):
    confluence_vector_store = FAISS.load_local(confluence_index_path, multi_lingual_embedder(),
                                               allow_dangerous_deserialization=True)
    retriever = confluence_vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return {"Documents": retriever.invoke(input)}


@app.post("/confluence")
@log_llm_report_time
@exception_handling
def confluence_llm_request(req: LLMRequest):
    start_total = time.time()

    start = time.time()
    confluence_vector_store = get_confluence_vec_store(req.faiss_index_path)
    logger.info(f"Time loading Vectorstore: {time.time() - start:.4f} seconds")

    llm = Llama3().create()

    start = time.time()
    docs = confluence_vector_store.similarity_search_with_score(req.input, k=req.k)
    logger.info(f"Time for Similarity Search: {time.time() - start:.4f} seconds")

    start = time.time()
    sorted_docs = sorted(docs, key=lambda x: x[1], reverse=False)
    logger.info(f"Time to sort: {time.time() - start:.4f} seconds")

    start = time.time()
    result = llm.invoke(f"Frage: {req.input}. Lasse keine relevanten Informationen weg! \n Context: {sorted_docs}")
    logger.info(f"Time for LLM call: {time.time() - start:.4f} seconds")
    logger.info(f"Total duration: {time.time() - start_total:.4f} seconds")
    logger.info(f"Result: {result}")
    return {"Result": result}


@app.post("/papers")
@log_llm_report_time
@exception_handling
def paper_llm_request(req: LLMRequestPapers):
    start_total = time.time()

    start = time.time()
    paper_vector_store = get_paper_vec_store(req.faiss_index_path)
    logger.info(f"Time loading Vectorstore: {time.time() - start:.4f} seconds")

    llm = Llama3().create()

    start = time.time()
    docs = paper_vector_store.similarity_search_with_score(req.input, k=req.k)
    logger.info(f"Time for Similarity Search: {time.time() - start:.4f} seconds")

    start = time.time()
    sorted_docs = sorted(docs, key=lambda x: x[1], reverse=False)
    for k, v in sorted_docs:
        print(k, v)
    logger.info(f"Time to sort: {time.time() - start:.4f} seconds")

    start = time.time()
    result = llm.invoke(f"Frage: {req.input}. Lasse keine relevanten Informationen weg! \n Context: {sorted_docs}")
    logger.info(f"Time for LLM call:: {time.time() - start:.4f} seconds")
    logger.info(f"Total duration: {time.time() - start_total:.4f} seconds")
    logger.info(f"Result: {result}")
    return {"Result": result}


@app.get("/gen_erp_index")
def gen_erp_index(index_type: Literal["text", "img"]):
    erp_handbook_index(erp_handbook_index_path(index_type), new_index=True)


@app.post("/erp")
@log_llm_report_time
@exception_handling
def erp_llm_request(req: LLMRequest):
    documents = retrieve_docs_from_erp_handbook(query=req.input, index_type="text")
    llm = Llama3().create()

    result = llm.invoke(paper_prompt(req.input, documents))
    image_documents = retrieve_docs_from_erp_handbook(query=result, index_type="img")

    llm_relevant_docs = llm.invoke(document_retrieval_prompt(result, image_documents))
    image_paths = re.findall(r'rag_app/.*?\.png', llm_relevant_docs)
    bin_images = image_from_path(image_paths)
    logger.info(f"Result: {result}")
    images_as_string = "\n Bilder:\n" + bin_images_to_text(bin_images)
    return {"Result": result + images_as_string}


@app.post("/get_paper_images")
@log_llm_report_time
@exception_handling
def get_paper_images(req: PageRequest):
    pages = req.pages
    images = get_erp_images(pages)
    response_text = ""
    for img in images:
        response_text += f"![{img['filename']}]({img['image_base64']})\n"
    return response_text


@app.get("/gen_paper_descriptions")
@log_llm_report_time
@exception_handling
def gen_paper_descriptions():
    generate_paper_image_descriptions()
    return {"Successful": True}


# ToDo Endpoint for Excel AI Analysis

@app.get("/send_mail")
@log_llm_report_time
@exception_handling
def send_mail(email_content, recipient):
    llm = Phi4_friendly().create()

    result = llm.invoke(email_prompt(email_content))
    subject_match = re.search(r'^subject:\s*(.+)', result, re.MULTILINE | re.IGNORECASE)

    subject = subject_match.group(1).strip() if subject_match else None

    text_match = re.search(r'^mail:\s*(.*)', result, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    if text_match:
        start = text_match.start(1)
        text = result[start:].strip()
    else:
        text = None
    EmailService().send_mail(subject, text, recipient)


if __name__ == "__main__":
    pass
