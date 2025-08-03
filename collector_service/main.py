"""
Description:
Author:         Timm Straub
E-Mail:
Version:        0.1
Created at:     2025/08/03
Last change:    2025/08/03
"""

from glob import glob

from fastapi import FastAPI

# from models import PaperQuery
from services.pdf_text_extractor import extract_pdf_texts
from services.postgres_service import save_pdf_in_db
from utils.paths import PDF_BASE_PATH

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Successful"}


# @app.post("/fetch_and_save_papers")
# async def fetch_and_save_papers(query: PaperQuery):
#     """
#     API-Endpoint to fetch and save papers in a csv file.
#     """
#     kwargs = query.model_dump()
#     fetch_and_save_top_100_papers(**kwargs)
#     return {"message": f"Top {kwargs['max_results']} AI papers have been fetched and saved."}


@app.get("/extract_and_save")
def extract_and_save():
    for file_path in glob(PDF_BASE_PATH + "/*"):
        text = extract_pdf_texts(file_path)
        save_pdf_in_db(file_path, text)
    return {"message": "OK"}

# if __name__ == "__main__":
#     extract_texts_from_path()
