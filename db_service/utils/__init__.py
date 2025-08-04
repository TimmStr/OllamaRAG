import os

from dotenv import load_dotenv

from utils.constants import HOST, USER, PASSWORD, DB_NAME, TIMESCALE_HOST, TIMESCALE_USER, TIMESCALE_PASSWORD, \
    TIMESCALE_DB_NAME


def timescaledb_config():
    load_dotenv()
    return {
        HOST: os.getenv(TIMESCALE_HOST),
        USER: os.getenv(TIMESCALE_USER),
        PASSWORD: os.getenv(TIMESCALE_PASSWORD),
        DB_NAME: os.getenv(TIMESCALE_DB_NAME)
    }
