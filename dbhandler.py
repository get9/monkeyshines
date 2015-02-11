import sqlite3
import os.path

class dbhandler:
    def __init__(self, filename):
        self.fname = filename

        # If file exists, then it will make a new connection, otherwise sqlite3
        # will make a new file.
        if not os.path.isfile(filename):
            self.create_db()

    # Runs the create statements
    def create_db(self):
        # XXX Eventually want to create a separate database.
        create_blacklist = """
            CREATE TABLE blacklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT
            )
            """
        create_urls = """
            CREATE TABLE url_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                hash TEXT,
                status_code INTEGER
            )
            """
        create_link_structure = """
            CREATE TABLE link_structure (
                inlink INTEGER,
                outlink INTEGER,
                FOREIGN KEY(inlink) REFERENCES url_list(id),
                FOREIGN KEY(outlink) REFERENCES url_list(id)
            )
            """
        # Create the tables
        with self.getdbconn() as con:
            curs = con.cursor()
            curs.execute(create_blacklist)
            curs.execute(create_urls)
            curs.execute(create_link_structure)

    # Gets a unique connection to the database (for multithreading).
    def getdbconn(self):
        return sqlite3.connect(self.fname)
