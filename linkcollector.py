from dbhandler import dbhandler
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, urlunsplit
from urlobj import URLObj

# One copy of this class per thread, so doesn't need to be thread-safe.
class LinkCollector:
    def __init__(self, dbhandle):
        self.dbhandle = dbhandle
        self.conn = dbhandle.getdbconn()

    # Main method that is called by the crawler object.
    def parse_links(self, fromurl, html):
        return self.filter_links(self.get_links(fromurl, html))

    # Only gets link from the static HTML
    # XXX: Currently only looking at href, nothing else.
    def get_links(self, fromurlo, html):
        # Get the base URL from which the HTML came from.
        baseurl = urlsplit(fromurlo.url)
        bshtml = BeautifulSoup(html)
        all_links = []
        hreflinks = []
        # Only gets href attrs
        for l in bshtml.find_all("a"):
            hreflinks.append(l['href'])
        # Can implement more link getters as needed.

        # Add in netloc for relative paths if it's missing
        all_links = all_links + hreflinks
        urls = []
        for link in all_links:
            urlo = URLObj(link)
            splitted = urlsplit(urlo.url)

            # It's a relative link.
            if splitted[1] is None:
                splitted[1] = baseurl

            # It's probably a domain, so we need to parse the robots.txt.
            elif splitted[2] == "" and splitted[3] == "" and splitted[4] == "":
                urlo.is_domain = True

            urlo.url = urlunsplit(splitted)
            urls.append(urlo)

        return urls
    
    # Filters links only, does not do anything else with them.
    def filter_links(self, links):
        # Keep adding stuff here to filter it out.
        links = filter(self.f_not_in_blacklist, links)
        links = filter(self.f_not_in_db, links)
    
        return links
    
    # Return True if link is not on blacklist.
    def f_not_in_blacklist(self, link):
        for site in self.dbhandle.get_blacklist():
            if site in link:
                return False
        return True

    # Return True if not in db already.
    def f_not_in_db(self, url):
        return self.db.has_url(url)
