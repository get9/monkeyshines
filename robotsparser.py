import requests
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
        return resp.status_code == requests.codes.ok

    # Actually parse the file.
    def parse(self):
        blackpaths = []
        resp = fetch(URLObj(join(self.domain, 'robots.txt')))
        for line in resp.text.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                continue
            elif line is None:
                continue
            elif line.startswith('Disallow'):
                badpath = line.split(':')[1].strip().strip('/')
                blackpaths.append(badpath)

        return [join(self.domain, b) for b in blackpaths]
