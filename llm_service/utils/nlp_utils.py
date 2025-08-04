import re
from typing import List

from langchain_core.documents import Document

from utils.logging_config import exception_handling


def filter_stop_words(text: str) -> str:
    import nltk
    from nltk.corpus import stopwords
    nltk.download('punkt', quiet=True)
    words = text.lower().split()
    german_stop_words = stopwords.words('german')
    return " ".join([word for word in words if word not in german_stop_words])


def filter_signs(text: str) -> str:
    return "".join(c for c in text if c.isalpha() or c.isspace())


def clean_text(document: Document) -> Document:
    document.page_content = re.sub(r'[^a-zA-Z0-9,.+\-*/€$ßäöüÄÖÜ%\s]', '', document.page_content.lower())
    return document


def get_overlap(current_chunk, overlap):
    words = " ".join(current_chunk).split()
    overlap_words = words[-overlap:] if overlap < len(words) else words
    current_chunk = [" ".join(overlap_words)]
    current_length = len(overlap_words)
    return current_chunk, current_length


@exception_handling
def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List:
    from nltk import sent_tokenize
    sentences = sent_tokenize(text)
    chunks, current_chunk = [], []
    current_length = 0

    for sentence in sentences:
        sentence_len = len(sentence.split())

        if current_length + sentence_len > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk, current_length = get_overlap(current_chunk, overlap) if overlap > 0 else ([], 0)

        current_chunk.append(sentence)
        current_length += sentence_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return [" ".join(chunk.split()) for chunk in chunks]
