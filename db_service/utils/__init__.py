import os

from dotenv import load_dotenv


def timescaledb_config():
    load_dotenv()
    return {
        "host": os.getenv('POSTGRES_HOST'),
        "user": os.getenv('POSTGRES_USER'),
        "password": os.getenv('POSTGRES_PASSWORD'),
        "dbname": os.getenv('POSTGRES_DB')
    }
