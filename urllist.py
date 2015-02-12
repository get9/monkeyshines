import logging
import threading

class URLList:
    def __init__(self, dbhandle):
        self.db = dbhandle
        self.ulist = set(self.__init_ulist())
        
    # Add url to the url list
    def append(self, urlo):
        with threading.Lock():
            self.ulist.add(urlo.xhash)

        with self.db.getdbconn() as con:
            add_url = "INSERT INTO url_list (url, hash, status_code) values (?, ?, ?)"
            curs = con.cursor()
            curs.execute(add_url, (urlo.url, urlo.xhash, urlo.status_code))

    # Check if value is in the Url list via hash
    def __contains__(self, urlo):
        in_list = False
        with threading.Lock():
            in_list = urlo.xhash in self.ulist

        return in_list

    # Get the number of url's seen so far.
    def __len__(self):
        with self.db.getdbconn() as con:
            count_url = "SELECT COUNT(*) FROM url_list"
            curs = con.cursor()
            curs.execute(count_url)
            return curs.fetchone()[0]

    def __init_ulist(self):
        with self.db.getdbconn() as con:
            hash_url = "SELECT hash FROM url_list"
            curs = con.cursor()
            curs.execute(hash_url)
            return [x[0] for x in curs.fetchall()]
