from fetcher import fetch
from robotsparser import RobotsParser
from linkcollector import LinkCollector
from workqueue import WorkQueue

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
        if not rp.robots.exists():
            print("couldn't find robots.txt from www.uky.edu")
        else:
            blacklinks = rp.parse()
            for u in blacklinks:
                self.db.add_to_blacklist(u)

        # Start crawl of baseurl.
        resp = fetch(baseurl)
        links = self.collector.parse_links(baseurl, resp.content)
        for l in links:
            queue.enqueue(l)

        # Repeat until queue is empty (gonna take a looooooong time...)
        while not queue.empty():
            resp = fetch(baseurl)
            links = self.collector.parse_links(baseurl, resp.content)
            for l in links:
                queue.enqueue(l)
