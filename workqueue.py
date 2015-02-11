from multiprocessing import Queue
from urlobj import URLObj

class WorkQueue():
    def __init__(self):
        # Specify maxsize when multithreading.
        self.queue = Queue()

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
        with open('queuedsites.txt', 'w') as f:
            while not self.empty():
                u = self.dequeue()
                f.write('{}${}${}${}${}${}\n'.format(u.url, u.xhash, u.status_code,
                    u.timedout, u.to_enqueue, u.is_domain))

    # Only called at the beginning; assumes we were interrupted in the middle of a run.
    def load(self):
        with open('queuedsites.txt', 'r') as f:
            for line in f:
                line = line.split('$')
                u = URLObj(line[0])
                u.xhash = line[1]
                u.status_code = line[2]
                u.timedout = line[3]
                u.to_enqueue = line[4]
                u.is_domain = line[5]
                self.enqueue(u)
