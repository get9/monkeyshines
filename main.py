#!/usr/bin/env python3

import sys
from crawler import Crawler

def main(baseurl):
    c = Crawler('ukysites.db')
    c.crawl(baseurl)

main(sys.argv[1])
