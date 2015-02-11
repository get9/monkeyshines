import sqlite3
import os.path

class dbhandler:
    def __init__(self, filename):
        self.fname = filename

        # If file exists, then it will make a new connection, otherwise sqlite3
        # will make a new file.
        if os.path.isfile(filename):
            self.create_db()

    # Count the number of URLs seen thus far.
    def get_url_count(self):
        get_urlcount = "SELECT COUNT(*) FROM url_list"
        with self.getdbconn().cursor() as curs:
            curs.execute(get_urlcount)
            return curs.fetchone()[0]

    # Insert URL into the db.
    def add_url(urlo):
        insert_url = "INSERT INTO url_list (url, hash) VALUES (?, ?)"
        with self.getdbconn().cursor() as curs:
            curs.execute(insert_url, (urlo.url, urlo.xhash))

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
                FOREIGN KEY(inlink) REFERENCES url_list(id),
                FOREIGN KEY(outlink) REFERENCES url_list(id)
            )
            """
        # Create the tables
        with self.getdbconn().cursor() as curs:
            curs.execute(create_blacklist)
            curs.execute(create_urls)
            curs.execute(create_link_structure)

    # Gets a unique connection to the database (for multithreading).
    def getdbconn(self):
        return sqlite3.connect(self.fname)

    # Checks if link is already in db
    def has_url(self, url):
        check_db = "SELECT * FROM url_list WHERE hash = ?"
        with self.getdbconn().cursor() as curs:
            curs.execute(check_db, url.xhash)
            return curs.fetchone() is None

    # Add a url to the blacklist.
    def add_to_blacklist(self, url):
        add_to_list = "INSERT INTO blacklist (domain) VALUES (?)"
        with self.getdbconn().cursor() as curs:
            curs.execute(add_to_list, url)
