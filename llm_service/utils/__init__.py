import glob
import os
import re
from typing import List, Tuple

import natsort
from dotenv import load_dotenv
from langchain_core.documents import Document

from utils.constants import MAIL_USER, MAIL_HOST, MAIL_PASSWORD, MAIL_PORT
from utils.logging_config import exception_handling
from utils.paths import PAPERS_OUTPUT_IMAGES, PAPERS_OUTPUT


def mail_config():
    load_dotenv()
    return {
        MAIL_HOST: os.getenv(MAIL_HOST),
        MAIL_USER: os.getenv(MAIL_USER),
        MAIL_PASSWORD: os.getenv(MAIL_PASSWORD),
        MAIL_PORT: os.getenv(MAIL_PORT)
    }


@exception_handling
def extract_page_number(llm_response: str) -> List:
    pages = []
    for match in re.findall(r'Page (\d+(?:-\d+)?)', llm_response):
        if '-' in match:
            start, end = map(int, match.split('-'))
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(match))
    return list(set(pages))


@exception_handling
def print_retrieved_docs(docs: list):
    for doc, score in docs:
        print("Documentcontent:", doc.page_content)
        print("Meta:", doc.metadata)
        print("Score:", score)
        print("---")


@exception_handling
def remove_repeated_first_line(input_str: str) -> str:
    lines = input_str.splitlines()

    if not lines:
        return input_str

    first_line = lines[0]
    cleaned_lines = [first_line]

    i = 1
    while i < len(lines) and lines[i] == first_line:
        i += 1
    cleaned_lines.extend(lines[i:])
    return "\n".join(cleaned_lines)


@exception_handling
def delete_repeating_lines_from_docs(docs: list) -> List[Tuple[Document, float]]:
    for k, v in docs:
        k.page_content = remove_repeated_first_line(k.page_content)
    return docs


@exception_handling
def bin_images_to_text(images):
    response_text = ""
    for img in images:
        response_text += f"![{img['filename']}]({img['image_base64']})\n"
    return response_text


@exception_handling
def get_erp_image_paths():
    return natsort.natsorted(glob.glob(os.path.join(PAPERS_OUTPUT_IMAGES, f"page_*")))


@exception_handling
def get_erp_text_paths():
    return natsort.natsorted(glob.glob(os.path.join(PAPERS_OUTPUT, f"page_*")))
