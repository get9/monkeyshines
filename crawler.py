from fetcher import fetch
from robotsparser import RobotsParser
from linkcollector import LinkCollector
from workqueue import WorkQueue
from dbhandler import dbhandler
from urlobj import URLObj
from blacklist import Blacklist
from urllist import URLList
from multiprocessor_worker import process_url
from multiprocessing import Pool

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
            pool = Pool(processes=3)
            pool.apply(process_url, (self.queue, self.db, self.urllist,
                                     self.blacklist))
            
        except Exception as ex:
            logging.debug("Encountered an exception", exc_info=True)
            self.queue.dump()
            sys.exit(1)
