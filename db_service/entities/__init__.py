from pydantic import BaseModel


class PaperClass(BaseModel):
    filename: str
    content: str
    title: str
    summary: str
    authors: str
    published: str
    url:str
    pdf_url: str
    file_path: str
