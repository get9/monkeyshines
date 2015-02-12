import logging

# Specific class for blacklist handling. Broken out of dbhandler
class Blacklist:
    def __init__(self, dbhandle):
        self.db = dbhandle
        self.blacklist = self.__init_blacklist()

    # Add to blacklist
    def append(self, site):
        logging.info("Adding {} to blacklist".format(site))
        self.blacklist.append(site)
        with self.db.getdbconn() as con:
            curs = con.cursor()
            add_site = "INSERT INTO blacklist (domain) VALUES (?)"
            curs.execute(add_site, (site,))

    # Check membership
    def __contains__(self, site):
        return site in self.blacklist

    def __init_blacklist(self):
        with self.db.getdbconn() as con:
            curs = con.cursor()
            get_sites = "SELECT domain FROM blacklist"
            curs.execute(get_sites)
            return [s for s in curs.fetchall()]
