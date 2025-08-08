import re
from typing import List, Tuple

from langchain_core.documents import Document

from utils import get_erp_text_paths
from utils.logging_config import exception_handling


@exception_handling
def extract_page_numbers_from_text(text: str) -> List[str]:
    return re.findall(r'Seite (\d+)', text)


@exception_handling
def delete_empty_rows(text: str) -> str:
    return re.sub(r'(\n\s*){2,}', '\n\n', text)


@exception_handling
def merge_pages_to_text() -> str:
    full_text = ""
    for path in get_erp_text_paths():
        with open(path, "r") as f:
            lines = f.readlines()
            lines_cleaned = [lines[4]]
            lines_cleaned.extend(lines[7:])
            text = "".join(lines_cleaned)
            full_text += (text + "\n\n")
    return full_text


@exception_handling
def get_start_and_end_of_paragraph(text, header_names, i) -> Tuple[int, int]:
    from_index = text.find(header_names[i].split(" /// ")[-1] + " \n")
    if i < len(header_names) - 1:
        return from_index, text.find(header_names[i + 1].split(" /// ")[-1] + " \n")
    return from_index, len(text)


def create_doc(paragraph: str, pages: list) -> Document:
    return Document(
        page_content=paragraph,
        metadata={"pages": list(map(int, pages))}
    )


@exception_handling
def gen_text_docs() -> List[Document]:
    """Created documents for each chapter"""
    text = delete_empty_rows(merge_pages_to_text()).replace("  ", " ")
    headers, header_pages = zip(*get_filtered_headers().items())
    documents = []
    for i, (header, pages_for_header) in enumerate(zip(headers, header_pages)):
        from_index, to_index = get_start_and_end_of_paragraph(text, headers, i)

        paragraph = text[from_index:to_index].replace(
            header.split(" /// ")[-1] + " \n",
            (("Kapitel:" + header + "\n") * 5)
        )
        paragraph = paragraph.replace("///", "-")

        pages = [pages_for_header] + extract_page_numbers_from_text(paragraph)

        if paragraph.count("\n") > 5:
            documents.append(create_doc(paragraph, pages))
        text = text[to_index:]
    return documents


if __name__ == "__main__":
    chapter_dict = gen_text_docs()
    print(chapter_dict)
