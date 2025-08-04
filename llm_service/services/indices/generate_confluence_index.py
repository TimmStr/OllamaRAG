import glob
import os
from typing import List, Tuple, Dict

from bs4 import BeautifulSoup
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from entities import TextSplitterSingleton
from entities.embedding import multi_lingual_embedder
from utils.logging_config import exception_handling_raise_e, exception_handling
from utils.nlp_utils import clean_text
from utils.paths import CONFLUENCE_HTML_PAGES


class ConfluenceVecStoreSingleton:
    _instances: Dict[str, FAISS] = {}

    @classmethod
    def get_instance(cls, faiss_index_path: str, new_index: bool) -> FAISS:
        if faiss_index_path in cls._instances:
            return cls._instances[faiss_index_path]

        if not os.path.exists(faiss_index_path) or new_index:
            vector_db = FAISS.from_documents(get_confluence_docs(), multi_lingual_embedder())
            vector_db.save_local(faiss_index_path)
        else:
            vector_db = FAISS.load_local(
                faiss_index_path,
                multi_lingual_embedder(),
                allow_dangerous_deserialization=True
            )

        cls._instances[faiss_index_path] = vector_db
        return vector_db


@exception_handling_raise_e
def filter_html_tags(html_content: str) -> Tuple[str, str]:
    soup = BeautifulSoup(html_content, 'html.parser')
    heading = soup.find('h1')
    # Entferne Scripts, Styles und unwichtige Tags
    for tag in soup(['script', 'style', 'header', 'nav', 'aside']):
        tag.decompose()

    # Extrahiere den Text
    text = soup.get_text(separator='\n', strip=True)
    return text, heading


def create_confluence_doc(heading: str, chunk: str, file_path: str) -> Document:
    return Document(
        page_content=f"Dateiname: {heading}\n{chunk}",
        metadata={"source": file_path}
    )


def read_html_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@exception_handling
def html_to_text_chunks(file_path: str, index) -> List[Document]:
    text_splitter = TextSplitterSingleton.get_instance()
    if os.path.splitext(file_path)[1].lower() == ".html":
        filtered_text, heading = filter_html_tags(read_html_content(file_path), index)
        if filtered_text.strip():
            chunks = text_splitter.split_text(filtered_text)
            return [create_confluence_doc(heading, chunk, file_path) for chunk in chunks]
    text_loader = TextLoader(file_path)
    docs = text_loader.load()
    return text_splitter.split_documents(docs)


@exception_handling
def get_confluence_docs() -> List[Document]:
    all_docs = []
    for index, file_path in enumerate(glob.glob(CONFLUENCE_HTML_PAGES + "/*.html", recursive=True)):
        documents = html_to_text_chunks(file_path, index)
        if documents:
            all_docs.extend([clean_text(doc) for doc in documents])
    return all_docs


@exception_handling
def get_confluence_vec_store(faiss_index_path: str, new_index: bool = False) -> FAISS:
    return ConfluenceVecStoreSingleton.get_instance(faiss_index_path, new_index)