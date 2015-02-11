from fetcher import fetch
from robotsparser import RobotsParser
from linkcollector import LinkCollector
from workqueue import WorkQueue
from dbhandler import dbhandler
from urlobj import URLObj
from blacklist import Blacklist
from urllist import URLList

import traceback
import os.path
import sys

class Crawler:
    def __init__(self, dbfname):
        self.db = dbhandler(dbfname)
        self.dbname = dbfname
        self.queue = WorkQueue()

        # Need to initialize workqueue if it was dumped previously.
        if os.path.isfile('queuedsites.txt'):
            print("loading work queue")
            self.queue.load()

        self.collector = LinkCollector(self.db)
        self.blacklist = Blacklist(self.db)
        self.urllist = URLList(self.db)

    # Entry point for main crawl.
    def crawl(self, baseurl):
        # Need to parse robots.txt from baseurl.
        rp = RobotsParser(baseurl)
        if rp.exists():
            blacklinks = rp.parse()
            for u in blacklinks:
                self.blacklist.append(u)
        else:
            print("couldn't find robots.txt from www.uky.edu")

        # Start crawl of baseurl.
        try:
            base = URLObj(baseurl)
            resp = fetch(base)
            links = self.collector.parse_links(base, resp.content)
            for l in links:
                if l not in self.urllist:
                    self.urllist.append(l)
                    self.queue.enqueue(l)

            # Repeat until queue is empty (gonna take a looooooong time...)
            while not self.queue.empty():
                newurl = self.queue.dequeue()
                resp = fetch(newurl)

                # Can be None if fetch times out
                if resp is None:
                    continue

                links = self.collector.parse_links(newurl, resp.content)
                for l in links:
                    if l not in self.urllist:
                        self.urllist.append(l)
                        self.queue.enqueue(l)
        except Exception as ex:
            traceback.print_exc()
            self.queue.dump()
            sys.exit(1)
