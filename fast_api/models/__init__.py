import os
from typing import Optional

from pydantic import BaseModel

from utils.paths import DATA


class PaperQuery(BaseModel):
    search_query: Optional[str] = "cat:cs.AI"
    max_results: Optional[int] = 100
    start_index: Optional[int] = 0
    filename: Optional[str] = os.path.join(DATA, "top_100_ai_papers.csv")
    save_dir: Optional[str] = os.path.join(DATA, "pdfs")
    mode: Optional[str] = "w+"
