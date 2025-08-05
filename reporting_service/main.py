"""
Description:    The app is used to create daily and monthly reports. To create the reports, the data is loaded from the
                Postgres database, packed into Excel files and, in the case of the daily report, sent to the managers
                in the form of an email.
Author:         Timm Straub
Version:        0.1
Created at:     2024/08/05
Last change:    2025/08/05
"""

import datetime
import glob
import os.path
from contextlib import asynccontextmanager

from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from starlette.responses import FileResponse

from connections.mailserver_connection import EmailService
from connections.smb_connection import SmbService
from utils import SMB_SERVER_PATH, load_smb_config
from utils.logging_config import log_report_time

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


@app.get("/")
async def root(test: bool = False) -> dict:
    if test:
        return {"message": "Test"}
    return {"message": "Root"}


@app.get("/annually_report")
@scheduler.scheduled_job('interval', seconds=21600)
@log_report_time
def annually_report() -> dict:
    # ToDo create Report
    folder_year = "2025"
    smb_config = load_smb_config()

    smb_service = SmbService()
    for file_path in glob.glob(os.path.join(f"{folder_year}", "*")):
        smb_service.mk_dir(os.path.join(smb_config.get(SMB_SERVER_PATH), folder_year))
        file_path_splitted = "\\".join(file_path.split("/"))
        smb_service.file_to_server(file_path, f"{smb_config.get(SMB_SERVER_PATH)}\\{file_path_splitted}")
    return {"message": "successful"}


@app.get("/daily_report")
@scheduler.scheduled_job('cron', hour=6, minute=35)
@log_report_time
def daily_report(config: str = "KPI_MAIL") -> dict:
    # ToDo create Report
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=1)
    path = ""
    EmailService(config).send_daily_report_mail(start_date=start_date, end_date=end_date, file_path=path)
    return {"message": "successful"}


@app.get('/customer_behavior_report')
@scheduler.scheduled_job('cron', day=1, hour=4)
@log_report_time
def customer_behavior_report():
    # ToDo create Report
    return {"message": "successful"}


@app.get('/csv_files')
def csv_files():
    # ToDo create csv files
    filename = "xyz.csv"
    file_response = FileResponse(filename, media_type='application/octet-stream', filename=filename)
    # os.remove(filename)
    return file_response


@app.get("/daily_mail")
@scheduler.scheduled_job('cron', hour=6, minute=40)
@log_report_time
def send_daily_mail():
    # ToDo create csv files/plot
    filename = "yesterday_report.csv"
    image_path = ""
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()

    recipients = ["t.straub@xyz.de", "m.mustermann@xyz.de"]
    subject = "XYZ Report"
    EmailService().send_mail(subject, f"Report for {yesterday}", recipients, [image_path])


if __name__ == "__main__":
    send_daily_mail()
