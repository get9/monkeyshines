import requests
import logging
from fetcher import fetch
from os.path import join
from urlobj import URLObj
from urllib.parse import urljoin, urlsplit, urlunsplit

class RobotsParser:
    def __init__(self, domain):
        self.domain = domain

    # Check if the file even exists first.
    def exists(self):
        resp = fetch(URLObj(join(self.domain, 'robots.txt')))
        return (resp is not None) and (resp.status_code == requests.codes.ok)

    # Actually parse the file.
    def parse(self):
        logging.info("Parsing robots.txt")
        blackpaths = []
        resp = fetch(URLObj(join(self.domain, 'robots.txt')))
        if resp is not None:
            for line in resp.text.split('\n'):
                line = line.strip()
                if line.startswith('#'):
                    continue
                elif line is None:
                    continue
                elif line.startswith('Disallow'):
                    badpath = line.split(':')[1].strip().strip('/')
                    blackpaths.append(badpath)

            return [URLObj(join(self.domain, b)) for b in blackpaths]
