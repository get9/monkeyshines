import xxhash

def get_hash(url):
    return xxhash.xxh64(url).hexdigest()

class URLObj:
    def __init__(self, url):
        self.url = url
        self.xhash = get_hash(url)
        self.outlinks = []
        self.status_code = -1
        self.timedout = False
        # Used for image files, js files, etc. If this is False, then we don't
        # enqueue it, just add the URL to the db. This will be done in the
        # LinkCollector module.
        self.to_enqueue = True
        self.is_domain = False
