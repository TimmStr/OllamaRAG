import glob
import os
from typing import Tuple, List

import natsort
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document

from entities.embedding import multi_lingual_embedder
from services.papers.edit_headlines import gen_text_docs
from utils import delete_repeating_lines_from_docs, print_retrieved_docs
from utils.logging_config import exception_handling
from utils.nlp_utils import filter_signs
from utils.paths import FAISS_ERP_TEXT_IDX_FOLDER, FAISS_ERP_IMG_DESC_IDX_FILE, \
    FAISS_ERP_IMG_DESC_IDX_FOLDER, PAPERS_OUTPUT_IMAGE_DESCRIPTIONS


def extract_page_number_from_path(path: str) -> str:
    """Use the path of the image description to find out the page number of the image."""
    return os.path.basename(path).split(".")[0].split("_")[1]


def img_desc_path_to_img_path(image_description_path: str) -> str:
    """Uses the path of the image description to extract the path of the image."""
    return image_description_path.replace("/descriptions", "").replace(".txt", ".png")


def img_desc_to_str(image_description_path: str) -> str:
    """Reads text from file and appends it to a str that starts with the filename."""
    with open(image_description_path, "r") as f:
        text = os.path.basename(image_description_path).split(".")[0] + "\n"
        text += f.read()
        return text


def gen_img_desc_doc(text, image_description_path) -> Document:
    """Returns LangChain Document from the description and path."""
    return Document(
        page_content=text,
        metadata={
            "pages": extract_page_number_from_path(image_description_path),
            "path": img_desc_path_to_img_path(image_description_path)}
    )


def erp_handbook_index_path(index_type: str) -> str:
    if index_type == "img":
        return FAISS_ERP_IMG_DESC_IDX_FOLDER
    return FAISS_ERP_TEXT_IDX_FOLDER


@exception_handling
def gen_img_desc_docs() -> List:
    """Generates List of LangChain Documents."""
    documents = []
    for img_desc_path in natsort.natsorted(
            glob.glob(os.path.join(PAPERS_OUTPUT_IMAGE_DESCRIPTIONS, "p*"))):
        documents.append(gen_img_desc_doc(img_desc_to_str(img_desc_path), img_desc_path))
    return documents


@exception_handling
def gen_erp_handbook_index(folder_path: str) -> FAISS:
    """Generates a new FAISS index from LangChain Documents."""
    documents = gen_img_desc_docs() if folder_path == FAISS_ERP_IMG_DESC_IDX_FILE else gen_text_docs()
    vector_db = FAISS.from_documents(documents, multi_lingual_embedder())
    vector_db.save_local(folder_path)
    return vector_db


@exception_handling
def erp_handbook_index(folder_path: str, new_index=False) -> FAISS:
    """Returns FAISS index."""
    if not os.path.exists(os.path.join(folder_path, "index.faiss")) or new_index:
        return gen_erp_handbook_index(folder_path)
    return FAISS.load_local(folder_path, multi_lingual_embedder(), allow_dangerous_deserialization=True)


@exception_handling
def retrieve_docs_from_erp_handbook(query: str, index_type: str, verbose=False) -> List[
    Tuple[Document, float]]:
    """High level func to orchestrate the document retrieval from an index."""
    faiss_index = erp_handbook_index(erp_handbook_index_path(index_type))
    top_docs = faiss_index.similarity_search_with_score(filter_signs(query), k=20)
    sorted_documents = delete_repeating_lines_from_docs(sorted(top_docs, key=lambda x: x[1], reverse=False))
    if verbose:
        print_retrieved_docs(sorted_documents)
    return sorted_documents


if __name__ == "__main__":
    print(retrieve_docs_from_erp_handbook())
