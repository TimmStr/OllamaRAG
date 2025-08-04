from pydantic import BaseModel

from utils.paths import FAISS_CONFLUENCE_TEXTS_IDX_FOLDER, FAISS_PAPERS_TEXTS_IDX_FOLDER


class LLMRequest(BaseModel):
    input: str
    faiss_index_path: str = FAISS_CONFLUENCE_TEXTS_IDX_FOLDER
    k: int = 10


class PageRequest(BaseModel):
    pages: list


class LLMRequestPapers(BaseModel):
    input: str
    faiss_index_path: str = FAISS_PAPERS_TEXTS_IDX_FOLDER
    k: int = 10
