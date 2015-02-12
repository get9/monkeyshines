import logging

from linkcollector import LinkCollector
from robotsparser import RobotsParser
from fetcher import fetch

def process_url(q, dbhandle, urls, blacklist):
    while not q.empty():
        logging.debug("Queue size = {}".format(q.size()))
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
            
        links = LinkCollector(dbhandle).parse_links(newurl, resp.content)
        for l in links:
            urls.append(l)
            q.enqueue(l)
