from services.connections.postgres_timescaledb import PostgresTimescaleConnection
from utils.constants import PAPER_TABLE, FILENAME, CONTENT
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
        conn.execute(insert_paper_query(), (kwargs.get(FILENAME), kwargs.get(CONTENT)))
        conn.commit()


def insert_paper_into_table(**kwargs):
    if not table_exists(PAPER_TABLE):
        create_paper_table()
    insert_paper(**kwargs)
    return "Successful"

