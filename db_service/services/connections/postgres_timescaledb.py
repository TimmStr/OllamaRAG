import psycopg

from utils import timescaledb_config
from utils.logging_config import data_transfer_logging


class PostgresTimescaleConnection:
    @data_transfer_logging
    def __init__(self, verbose=False):
        self.conn = psycopg.connect(**timescaledb_config())
        if verbose:
            print("Connection established")

    def execute(self, query, params=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:
                return cursor.fetchall()
            return cursor.rowcount

    def commit(self):
        try:
            self.conn.commit()
        except Exception as e:
            print(f"Commit failed. Error: {e}")

    def __del__(self):
        if hasattr(self, "conn") and self.conn:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self, "conn") and self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Test
    try:
        with PostgresTimescaleConnection() as anlage_connection:
            res = anlage_connection.execute("""
            SELECT usename AS role_name,
                CASE
                    WHEN usesuper AND usecreatedb THEN
                        CAST('superuser, create database' AS pg_catalog.text)
                    WHEN usesuper THEN
                        CAST('superuser' AS pg_catalog.text)
                    WHEN usecreatedb THEN
                        CAST('create database' AS pg_catalog.text)
                    ELSE
                        CAST('' AS pg_catalog.text)
                END role_attributes
            FROM pg_catalog.pg_user
            ORDER BY role_name desc;""")
        print(res)
    except Exception as e:
        raise e
    finally:
        del anlage_connection
