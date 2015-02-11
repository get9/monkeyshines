from fetcher import fetch
from robotsparser import RobotsParser
from linkcollector import LinkCollector
from workqueue import WorkQueue
from dbhandler import dbhandler
from urlobj import URLObj

class Crawler:
    def __init__(self, dbfname):
        self.db = dbhandler(dbfname)
        self.dbname = dbfname
        self.queue = WorkQueue()
        self.collector = LinkCollector(self.db)

    # Entry point for main crawl.
    def crawl(self, baseurl):
        # Need to parse robots.txt from baseurl.
        rp = RobotsParser(baseurl)
        if rp.exists():
            blacklinks = rp.parse()
            for u in blacklinks:
                self.db.add_to_blacklist(u)
        else:
            print("couldn't find robots.txt from www.uky.edu")

        # Start crawl of baseurl.
        base = URLObj(baseurl)
        resp = fetch(base)
        links = self.collector.parse_links(base, resp.content)
        for l in links:
            queue.enqueue(l)

        # Repeat until queue is empty (gonna take a looooooong time...)
        while not queue.empty():
            newurl = queue.dequeue()
            resp = fetch(newurl)
            links = self.collector.parse_links(newurl, resp.content)
            for l in links:
                queue.enqueue(l)
