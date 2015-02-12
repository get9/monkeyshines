import threading
import logging
import re
from urllib.parse import urlsplit

# Specific class for blacklist handling. Broken out of dbhandler
class Blacklist:
    def __init__(self, dbhandle):
        self.db = dbhandle
        self.blist = set(self.__init_blist())

    # Add to blacklist
    def append(self, site):
        url = site.url
        with threading.Lock():
            self.blist.add(url.rstrip('/'))

        logging.debug("Adding {} to blacklist".format(url))
        with self.db.getdbconn() as con:
            curs = con.cursor()
            add_site = "INSERT INTO blacklist (domain) VALUES (?)"
            if not re.match('http:\/\/', url):
                if re.match('\/\/', url):
                    url = 'http:' + url
                else:
                    url = 'http://' + url
            curs.execute(add_site, (url.rstrip('/'),))

    # Check membership
    def __contains__(self, site):
        scheme, netloc, path, query, fragment = urlsplit(site.url)
        in_list = False
        with threading.Lock():
            in_list = netloc.rstrip('/') in self.blist
        return in_list

    def __init_blist(self):
        with self.db.getdbconn() as con:
            hash_url = "SELECT domain FROM blacklist"
            curs = con.cursor()
            curs.execute(hash_url)
            return [x[0] for x in curs.fetchall()]
