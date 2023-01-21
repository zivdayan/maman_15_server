import sqlite3
from os.path import isfile
from typing import Dict
import logging


class SQLiteDatabase:
    DB_NAME = 'FileServer.db'

    def __init__(self, logger, name=DB_NAME):
        self.conn = None
        self.cursor = None
        self.logger: logging.Logger = logger

        if name:
            self.open(name)

    def open(self, name):
        try:
            self.conn = sqlite3.connect(name);
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to database! Reason: {str(e)}")

    def init_db(self, tables: Dict[str, str]):
        for table_name, table_description in tables.items():
            self.create_table(table_name, table_description)

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def get(self, table, columns, limit=None):

        query = "SELECT {0} from {1};".format(columns, table)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows) - limit if limit else 0:]

    def create_table(self, table_name, table_description):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({table_description});"

        self.cursor.execute(query)

    def write(self, query, *args):
        self.cursor.execute(query, args)

    def update(self, query, *args):
        self.cursor.execute(query, args)

    def query(self, sql, *args):
        self.cursor.execute(sql, args)
