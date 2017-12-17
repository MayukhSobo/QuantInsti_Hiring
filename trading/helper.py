from queue import Queue


# https://stackoverflow.com/questions/1293966/best-way-to-obtain-indexed-access-to-a-python-queue-thread-safe
class IndexedQueue(Queue):
    def __getitem__(self, index):
        with self.mutex:
            return self.queue[index]
