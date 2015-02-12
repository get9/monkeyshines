from linkcollector import LinkCollector
from robotsparser import RobotsParser

def worker_thread(q, dbhandle, urls, blacklist):
    newurl = q.dequeue()

    # If domain, then need to add blacklist
    if newurl.is_domain:
        rp = RobotsParser(newurl.url)
        if rp.exists():
            blacklinks = rp.parse()
            for l in blacklinks:
                blacklist.append(l)

    resp = fetch(newurl)
    if resp is None:
        logging.warn("Could not fetch {}".format(newurl.url))
        
    links = LinkCollector(dbhandle).parse_links(newurl, resp.content)
    for l in links:
        urls.append(l)
        q.enqueue(l)
