import os

from dotenv import load_dotenv


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def title_to_filename(paper_title):
    return paper_title.replace(" ", "_").replace("/", "_") + ".pdf"


def filename_to_title(filename):
    return filename.replace("_", " ").replace("_")


def postgres_insert_address():
    load_dotenv()
    return os.getenv("POSTGRES_SERVICE_INSERT_PAPER")
