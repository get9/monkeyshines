from fetcher import fetch
from robotsparser import RobotsParser
from linkcollector import LinkCollector
from workqueue import WorkQueue
from dbhandler import dbhandler
from urlobj import URLObj
from blacklist import Blacklist
from urllist import URLList
from multiprocessor_worker import process_url

import threading
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
        thread_list = []
        try:
            for i in range(4):
                t = threading.Thread(target=process_url, args=(self.queue,
                                     self.db, self.urllist, self.blacklist))
                thread_list.append(t)

            for thread in thread_list:
                thread.start()

            for thread in thread_list:
                thread.join()
            
        except (KeyboardInterrupt, Exception):
            logging.debug("Encountered an exception", exc_info=True)
            self.queue.dump()
            sys.exit(1)
