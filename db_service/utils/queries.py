from utils.constants import PAPER_TABLE, PAPER_TITLE, PAPER_CONTENT, PAPER_ID, PAPER_SUMMARY, PAPER_AUTHORS, PAPER_PUBLISHED, PAPER_URL, \
    PAPER_PDF_URL, PAPER_FILE_PATH

CREATE_PAPER_TABLE_QUERY = f"""
    CREATE TABLE {PAPER_TABLE} (
        {PAPER_ID} SERIAL PRIMARY KEY,
        {PAPER_TITLE} text NOT NULL,
        {PAPER_CONTENT} text,
        {PAPER_SUMMARY} text,
        {PAPER_AUTHORS} text,
        {PAPER_PUBLISHED} date,
        {PAPER_URL} text,
        {PAPER_PDF_URL} text,
        {PAPER_FILE_PATH} text
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
        ({PAPER_TITLE}, {PAPER_CONTENT}, {PAPER_SUMMARY}, {PAPER_AUTHORS}, {PAPER_PUBLISHED}, {PAPER_URL}, {PAPER_PDF_URL}, {PAPER_FILE_PATH})
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s)
"""
