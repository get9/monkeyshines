import logging

from linkextractor import extract
from filterengine import filter_links
from robotsparser import RobotsParser
from fetcher import fetch

def process_url(q, dbhandle, urls, blacklist):
    try:
        while not q.empty():
            logging.info("Queue size = {}".format(q.size()))
            newurl = q.dequeue()

            # If domain, then need to add blacklist
            if newurl.is_domain:
                rp = RobotsParser(newurl.url)
                if rp.exists():
                    blacklinks = rp.parse()
                    if blacklinks:
                        for l in blacklinks:
                            blacklist.append(l)

            resp = fetch(newurl)
            if resp is None:
                logging.warn("Could not fetch {}".format(newurl.url))
                continue
                
            page_urls = extract(resp.content, newurl)
            for l in filter_links(page_urls, urls, blacklist):
                urls.append(l)
                q.enqueue(l)
    except Exception:
        logging.debug("Encountered an exception", exc_info=True)
