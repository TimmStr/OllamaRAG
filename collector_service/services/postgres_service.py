import os.path

import requests

from utils import postgres_insert_address
from utils.constants import SUMMARY, PUBLISHED, PDF_URL, TITLE, AUTHORS, URL, CONTENT, FILENAME, FILE_PATH


def save_pdf_in_db(content, title, summary, authors, published, url, pdf_url, file_path):
    payload = {
        FILENAME: os.path.basename(file_path),
        CONTENT: content,
        TITLE: title,
        SUMMARY: summary,
        AUTHORS: authors,
        PUBLISHED: published,
        URL: url,
        PDF_URL: pdf_url,
        FILE_PATH: file_path
    }
    response = requests.post(postgres_insert_address(), json=payload)
    print(response.status_code)
    print(response.json())


if __name__ == '__main__':
    save_pdf_in_db("xyz",
                   "test",
                   "That's the message.",
                   "karl, Peter",
                   "15-04-2025",
                   "http://www.xyz.com",
                   "http://www.xyz.com/pdf_file.pdf",
                   "data/pdfs"
                   )
