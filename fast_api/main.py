from fastapi import FastAPI

from models import PaperQuery
from services.load_influential_ai_papers import fetch_and_save_top_100_papers

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Successful"}


@app.post("/fetch_and_save_papers")
async def fetch_and_save_papers(query: PaperQuery):
    """
    API-Endpoint to fetch and save papers in a csv file.
    """
    kwargs = query.model_dump()
    fetch_and_save_top_100_papers(**kwargs)
    return {"message": f"Top {kwargs['max_results']} AI papers have been fetched and saved."}
