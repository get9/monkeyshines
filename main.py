#!/usr/bin/env python3

import sys
import logging
from crawler import Crawler

def configure_logger():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO, filename='crawl.log')
    logging.info('Configured logger')
    logging.getLogger('requests').setLevel(logging.WARNING)

def main(baseurl):
    configure_logger()
    c = Crawler('ukysites.db')
    c.crawl(baseurl)

main(sys.argv[1])
