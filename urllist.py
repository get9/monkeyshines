import logging

class URLList:
    def __init__(self, dbhandle):
        self.db = dbhandle
        
    # Add url to the url list
    def append(self, urlo):
        with self.db.getdbconn() as con:
            add_url = "INSERT INTO url_list (url, hash, status_code) values (?, ?, ?)"
            curs = con.cursor()
            curs.execute(add_url, (urlo.url, urlo.xhash, urlo.status_code))

    # Check if value is in the Url list via hash
    def __contains__(self, urlo):
        with self.db.getdbconn() as con:
            check_url = "SELECT * FROM url_list WHERE hash = ?"
            curs = con.cursor()
            curs.execute(check_url, (urlo.xhash,))
            return curs.fetchone() is not None

    # Get the number of url's seen so far.
    def __len__(self):
        with self.db.getdbconn() as con:
            count_url = "SELECT COUNT(*) FROM url_list"
            curs = con.cursor()
            curs.execute(count_url)
            return curs.fetchone()[0]
