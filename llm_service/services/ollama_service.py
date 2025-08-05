import time

from entities.ollama_entities import Llama3
from services.indices.generate_confluence_index import get_confluence_vec_store
from services.indices.generate_paper_index import get_paper_vec_store
from utils.constants import rag_prompt
from utils.logging_config import logger


def llm_request(req, paper_vec_store=True):
    start_total = time.time()
    vector_store = get_paper_vec_store(req.faiss_index_path) if paper_vec_store else get_confluence_vec_store(
        req.faiss_index_path)
    logger.info(f"Time loading Vectorstore: {time.time() - start_total:.4f} seconds")

    llm = Llama3().create()

    start = time.time()
    docs = vector_store.similarity_search_with_score(req.input, k=req.k)
    logger.info(f"Time for Similarity Search: {time.time() - start:.4f} seconds")

    start = time.time()
    sorted_docs = sorted(docs, key=lambda x: x[1], reverse=False)
    logger.info(f"Time to sort: {time.time() - start:.4f} seconds")

    start = time.time()
    result = llm.invoke(rag_prompt(req.input, sorted_docs))
    logger.info(f"Time for LLM call:: {time.time() - start:.4f} seconds")
    logger.info(f"Total duration: {time.time() - start_total:.4f} seconds")
    logger.info(f"Result: {result}")
    return result
