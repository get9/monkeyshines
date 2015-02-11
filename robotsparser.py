import requests
from fetcher import fetch
from urlobj import URLObj
from urllib.parse import urljoin, urlsplit, urlunsplit

class RobotsParser:
    def __init__(self, domain):
        self.domain = URLObj(domain)

    # Check if the file even exists first.
    def robots_exists(self):
        resp = fetch(urljoin(self.domain, 'robots.txt'))
        return resp.status_code == requests.codes.ok

    # Actually parse the file.
    def parse(self):
        blackpaths = []
        resp = fetch(urljoin(self.domain, 'robots.txt'))
        for line in resp.content:
            line = line.strip()
            if line.startswith('#'):
                continue
            elif line is None:
                continue
            elif line.startswith('Disallow'):
                blackpaths.append(line.split(':')[1].strip().rstrip('/'))

        return [urljoin(self.domain, b) for b in blackpaths]
