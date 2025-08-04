from pydantic import BaseModel


class PaperQuery(BaseModel):
    search_query: str
    max_results: int
    start_index: int
