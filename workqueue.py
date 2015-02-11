import multiprocessing.Queue

class WorkQueue:
    def __init__(self):
        # Specify maxsize when multithreading.
        self.queue = multiprocessing.Queue()

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
