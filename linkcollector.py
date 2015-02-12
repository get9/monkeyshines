from dbhandler import dbhandler
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, urlunsplit
from urlobj import URLObj
from blacklist import Blacklist

import os.path
import re
import logging

SKIP_FILES = ['.pdf', '.png', '.gif', '.jpg', '.jpeg', '.wmv', '.mp4', '.mp3']

# One copy of this class per thread, so doesn't need to be thread-safe.
class LinkCollector:
    def __init__(self, dbhandle):
        self.dbhandle = dbhandle
        self.conn = dbhandle.getdbconn()
        self.blacklist = Blacklist(dbhandle)
        self.urllist = URLList(dbhandle)

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
        # Only gets href attrs from <a> with href of uky.edu
        logging.info("Finding links in page")
        for l in bshtml.find_all("a", href=re.compile('.*uky\.edu.*')):
            hreflinks.append(l['href'])
        # Can implement more link getters as needed.

        # Add in netloc for relative paths if it's missing
        all_links = all_links + hreflinks
        urls = []
        for link in all_links:
            link = link.rstrip('/')

            # Skip any links to PDF's, images, etc.
            if os.path.splitext(link)[1] in SKIP_FILES:
                continue

            urlo = URLObj(link)
            scheme, netloc, path, query, fragment = urlsplit(urlo.url)

            # Skip empty URLs (however they got there...)
            if all(o is None for o in (scheme, netloc, path, query, fragment)):
                logging.info("Skipping empty URL")
                continue

            # Skip URLs that are just fragments.
            elif all(o is None for o in (scheme, netloc, path, query)):
                logging.info("Skipping frag'd URL")
                continue

            # Skip any domain that's not UKY.
            elif not re.search('uky.edu', netloc):
                logging.info("Skipping non-uky domain {}".format(link))
                continue

            # It's a relative link.
            elif scheme is None and netloc is None:
                urlo.url = urljoin((scheme, baseurl, path, query, fragment))
                logging.info("Canonicalizing URL: {} ---> {}".format(baseurl, urlo.url))

            # It's probably a domain, so we need to parse the robots.txt.
            elif path == "" and query == "" and fragment == "":
                urlo.is_domain = True

            urls.append(urlo)

        return urls
    
    # Filters links only, does not do anything else with them.
    def filter_links(self, links):
        # Keep adding stuff here to filter it out.
        links = filter(lambda x: x not in self.blacklist, links)
        links = filter(lambda x: x not in self.urllist, links)
    
        return links
