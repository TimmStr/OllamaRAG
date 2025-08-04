"""
Description:
Author:         Timm Straub
E-Mail:
Version:        0.1
Created at:     2025/08/03
Last change:    2025/08/03
"""

from contextlib import asynccontextmanager

from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from entities import PaperClass
from services.postgres_service import insert_paper_into_table
from utils.constants import PAPER_TITLE, PAPER_SUMMARY, PAPER_AUTHORS, PAPER_PUBLISHED, PAPER_URL, PAPER_PDF_URL, \
    PAPER_FILE_PATH, PAPER_CONTENT
from utils.logging_config import log_transfer_time

jobstores = {
    'default': MemoryJobStore()
}
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone='Europe/Berlin')


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


# @app.get("/postgres")
# @scheduler.scheduled_job('cron', hour=6, minute=5)
# @log_transfer_time
# def transfer_all(is_all_tables=False):
#     return func
@log_transfer_time
@app.post("/insert_paper")
async def insert_paper(paper_payload: PaperClass):
    print(f"Received file: {paper_payload.filename}")
    print(f"Content: {paper_payload.content[:50]}...")  # nur die ersten 50 Zeichen
    kwargs = {
        PAPER_TITLE: paper_payload.title,
        PAPER_CONTENT: paper_payload.content,
        PAPER_SUMMARY: paper_payload.summary,
        PAPER_AUTHORS: paper_payload.authors,
        PAPER_PUBLISHED: paper_payload.published,
        PAPER_URL: paper_payload.url,
        PAPER_PDF_URL: paper_payload.pdf_url,
        PAPER_FILE_PATH: paper_payload.file_path
    }
    print("result", insert_paper_into_table(**kwargs))
    return {"message": "OK"}
#
#
# @app.get("/update_views")
# @log_transfer_time
# @scheduler.scheduled_job('cron', hour=9, minute=0)
# def update_materialized_views(year=None):
#     # create_view(**kwargs)
#     return SUCCESSFUL_MESSAGE
#
#
# @app.get("/create_essential_indices")
# @log_transfer_time
# def create_essential_indices():
#     create_indices(**kwargs)
#     return SUCCESSFUL_MESSAGE
#
#
# if __name__ == "__main__":
#     transfer_cspro_tables()
#     pass
