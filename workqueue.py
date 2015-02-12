from multiprocessing import Manager
from urlobj import URLObj

import logging

class WorkQueue():
    def __init__(self):
        # Specify maxsize when multithreading.
        self.queue = Manager().Queue()
        self.loaded = False

    # Semantics:
    #     Puts 'urlo' into the queue. If there's no free space, it will block
    #     until there is free space.
    def enqueue(self, urlo):
        self.queue.put(urlo, True)

    # Semantics:
    #     Gets a urlobj from the queue. If there's nothing in the queue, it will
    #     block until there's something there. I don't expect this to block
    #     very often.
    def dequeue(self):
        return self.queue.get(True)

    def empty(self):
        return self.queue.empty()

    # Only called if we have an exception; writes the queue out to a file.
    def dump(self):
        logging.info("Dumping queue")
        with open('queuedsites.txt', 'w') as f:
            while not self.empty():
                u = self.dequeue()
                f.write('{}<>{}<>{}<>{}<>{}<>{}\n'.format(u.url, u.xhash, u.status_code,
                    u.timedout, u.to_enqueue, u.is_domain))

    # Only called at the beginning; assumes we were interrupted in the middle of a run.
    def load(self):
        logging.info("Loading queue")
        with open('queuedsites.txt', 'r') as f:
            for line in f:
                line = line.strip().split('<>')
                if not line:
                    continue

                # XXX Sometimes we have lines that aren't all the data from the URLObj?
                elif len(line) < 6:
                    logging.warn("Found queued URL with less than 6 params: {}".format(line[0]))
                    continue
                u = URLObj(line[0])
                u.xhash = line[1]
                u.status_code = int(line[2])
                u.timedout = bool(line[3])
                u.to_enqueue = bool(line[4])
                u.is_domain = bool(line[5])
                self.enqueue(u)
        self.queue.loaded = True
