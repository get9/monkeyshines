import re
import os.path
import logging

from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlunsplit
from urlobj import URLObj

# Extensions of files to skip
SKIP_FILES = ['.pdf', '.png', '.gif', '.jpg', '.jpeg', '.wmv', '.mp4', '.mp3', '.mov']

# Only gets link from the static HTML
# XXX: Currently only looking at href, nothing else.
def extract(html, fromurlo):
    # Get the base URL from which the HTML came from.
    bshtml = BeautifulSoup(html)

    # Only gets href attrs from <a> with href of uky.edu
    pageurls = []
    for l in bshtml.find_all("a"):
        pageurls.append(l.get('href'))

    # Fix any links we find and return them
    return fix_links(pageurls, urlsplit(fromurlo.url).netloc)

def fix_links(urls, domain):
    good_urls = []
    for url in urls:
        if url is None:
            continue

        scheme, netloc, path, query, fragment = urlsplit(url)
        is_domain = False

        # Skip anything that has a scheme other than HTTP
        if not re.match('https?', scheme, re.IGNORECASE):
            continue

        # Skip any links to PDF's, images, etc.
        elif os.path.splitext(path)[1] in SKIP_FILES:
            logging.debug("Skipping resource file: {}".format(url))
            continue

        # Skip empty URLs (however they got there...)
        elif all(not o for o in (scheme, netloc, path, query, fragment)):
            continue

        # Skip URLs that are just fragments.
        elif all(not o for o in (scheme, netloc, path, query)):
            logging.debug("Skipping frag'd URL: {}".format(url))
            continue

         # It's not a uky domain
        elif netloc and not re.match('.*uky.edu', netloc):
            logging.debug("Skipping non-UKY domain: {}".format(url))
            continue

        # Check if it's probably a domain; then we need to parse robots.txt
        elif all(not o for o in (path, query, fragment)):
            is_domain = True

        # Change relative URL to absolute.
        elif not scheme and not netloc:
            url = urlunsplit(('http', domain, path, query, fragment))
            logging.debug("Canonicalizing URL: {} ---> {}".format(path, url))
        
        # Append good url to return list
        urlo = URLObj(url)
        urlo.is_domain = is_domain
        good_urls.append(urlo) 
    return good_urls
