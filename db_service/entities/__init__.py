from pydantic import BaseModel


class PaperClass(BaseModel):
    filename: str
    content: str
