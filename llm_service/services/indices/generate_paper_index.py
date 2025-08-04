import glob
import os
from typing import List, Dict

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from entities import TextSplitterSingleton
from entities.embedding import multi_lingual_embedder
from utils.logging_config import exception_handling
from utils.nlp_utils import clean_text
from utils.paths import PAPERS


class PaperVecStoreSingleton:
    _instances: Dict[str, FAISS] = {}

    @classmethod
    def get_instance(cls, faiss_index_path: str, new_index: bool) -> FAISS:
        if faiss_index_path in cls._instances:
            return cls._instances[faiss_index_path]

        if not os.path.exists(faiss_index_path) or new_index:
            vector_db = FAISS.from_documents(get_paper_docs(), multi_lingual_embedder())
            vector_db.save_local(faiss_index_path)
        else:
            vector_db = FAISS.load_local(
                faiss_index_path,
                multi_lingual_embedder(),
                allow_dangerous_deserialization=True
            )

        cls._instances[faiss_index_path] = vector_db
        return vector_db


def create_paper_doc(heading: str, chunk: str, file_path: str) -> Document:
    return Document(
        page_content=f"Filename: {heading}\n{chunk}",
        metadata={"source": file_path}
    )


def read_txt_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@exception_handling
def text_to_chunks(file_path: str) -> List[Document]:
    text_splitter = TextSplitterSingleton.get_instance()
    text = read_txt_content(file_path)
    heading = os.path.basename(file_path).split(".")[0]
    if text.strip():
        chunks = text_splitter.split_text(text)
        return [create_paper_doc(heading, chunk, file_path) for chunk in chunks]
    text_loader = TextLoader(file_path)
    docs = text_loader.load()
    return text_splitter.split_documents(docs)


@exception_handling
def get_paper_docs() -> List[Document]:
    all_docs = []
    for file_path in glob.glob(PAPERS + "/*.txt", recursive=True):
        documents = text_to_chunks(file_path)
        if documents:
            all_docs.extend([clean_text(doc) for doc in documents])
    return all_docs


@exception_handling
def get_paper_vec_store(faiss_index_path: str, new_index: bool = False) -> FAISS:
    return PaperVecStoreSingleton.get_instance(faiss_index_path, new_index)
