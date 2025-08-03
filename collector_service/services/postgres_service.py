import requests

from utils import postgres_insert_address


def save_pdf_in_db(file_path, content):
    payload = {
        "filename": file_path,
        "content": content
    }
    response = requests.post(postgres_insert_address(), json=payload)
    print(response.status_code)
    print(response.json())

if __name__ == '__main__':
    save_pdf_in_db("xyz", "test")
