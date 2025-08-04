from connections.postgres_timescaledb import PostgresTimescaleConnection
from utils.constants import (PAPER_TABLE, PAPER_TITLE, PAPER_SUMMARY, PAPER_AUTHORS, PAPER_PUBLISHED, PAPER_URL,
                             PAPER_PDF_URL, PAPER_CONTENT, PAPER_FILE_PATH)
from utils.queries import table_exists_query, CREATE_PAPER_TABLE_QUERY, insert_paper_query


def table_exists(table):
    query = table_exists_query(table)
    with PostgresTimescaleConnection() as conn:
        result = conn.execute(query)
    return bool(result[0][0])


def create_paper_table():
    with PostgresTimescaleConnection() as conn:
        conn.execute(CREATE_PAPER_TABLE_QUERY)
        conn.commit()


def insert_paper(**kwargs):
    with PostgresTimescaleConnection() as conn:
        conn.execute(insert_paper_query(), (
            kwargs.get(PAPER_TITLE),
            kwargs.get(PAPER_CONTENT),
            kwargs.get(PAPER_SUMMARY),
            kwargs.get(PAPER_AUTHORS),
            kwargs.get(PAPER_PUBLISHED),
            kwargs.get(PAPER_URL),
            kwargs.get(PAPER_PDF_URL),
            kwargs.get(PAPER_FILE_PATH)))
        conn.commit()


def insert_paper_into_table(**kwargs):
    if not table_exists(PAPER_TABLE):
        create_paper_table()
    insert_paper(**kwargs)
    return "Successful"
