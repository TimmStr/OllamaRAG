from utils.constants import PAPER_TABLE, PAPER_TITLE, PAPER_CONTENT, PAPER_ID

CREATE_PAPER_TABLE_QUERY = f"""
    CREATE TABLE {PAPER_TABLE} (
        {PAPER_ID} SERIAL PRIMARY KEY,
        {PAPER_TITLE} text NOT NULL,
        {PAPER_CONTENT} text
    );
    """


def table_exists_query(table):
    return f"""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = '{table}'
    );
    """


def insert_paper_query():
    return f"""
    INSERT INTO {PAPER_TABLE}
        ({PAPER_TITLE}, {PAPER_CONTENT})
        VALUES 
        (%s, %s)
"""
