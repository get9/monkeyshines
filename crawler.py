from fetcher import fetch
from robotsparser import RobotsParser
from linkcollector import LinkCollector
from workqueue import WorkQueue
from dbhandler import dbhandler
from urlobj import URLObj
from blacklist import Blacklist
from urllist import URLList

import traceback
import logging
import os.path
import sys

class Crawler:
    def __init__(self, dbfname):
        self.db = dbhandler(dbfname)
        self.dbname = dbfname
        self.queue = WorkQueue()

        # Need to initialize workqueue if it was dumped previously.
        if os.path.isfile('queuedsites.txt'):
            logging.info('Loading work queue from cache')
            self.queue.load()

        self.collector = LinkCollector(self.db)
        self.blacklist = Blacklist(self.db)
        self.urllist = URLList(self.db)

    # Entry point for main crawl.
    def crawl(self, baseurl):
        if not self.queue.loaded:
            # Need to parse robots.txt from baseurl.
            rp = RobotsParser(baseurl)
            if rp.exists():
                logging.info('Parsing {}/robots.txt'.format(baseurl))
                blacklinks = rp.parse()
                for u in blacklinks:
                    self.blacklist.append(u)
            else:
                logging.warn("Couldn't find {}/robots.txt".format(baseurl))

            # Load baseurl, run it.
            try:
                base = URLObj(baseurl)
                resp = fetch(base)
                links = self.collector.parse_links(base, resp.content)
                for l in links:
                    self.urllist.append(l)
                    self.queue.enqueue(l)
            except Exception as ex:
                logging.debug("Encountered an exception", exc_info=True)
                self.queue.dump()
                sys.exit(1)

        # Start crawl of baseurl.
        try:
            # Repeat until queue is empty (gonna take a looooooong time...)
            while not self.queue.empty():
                newurl = self.queue.dequeue()

                # If newurl is a domain, then we need to check for the blacklist
                if newurl.is_domain:
                    logging.info("{} is likely a domain, getting robots.txt".format(newurl.url))
                    rp = RobotsParser(newurl.url)
                    if rp.exists():
                        blacklinks = rp.parse()
                        for u in blacklinks:
                            self.blacklist.append(u)
                    else:
                        logging.warn("Couldn't find {}/robots.txt".format(newurl.url))

                resp = fetch(newurl)

                # Can be None if fetch times out
                if resp is None:
                    logging.warn("Could not fetch {}".format(newurl.url))
                    continue

                links = self.collector.parse_links(newurl, resp.content)
                for l in links:
                    self.urllist.append(l)
                    self.queue.enqueue(l)

        except Exception as ex:
            logging.debug("Encountered an exception", exc_info=True)
            self.queue.dump()
            sys.exit(1)
