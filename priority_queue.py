
from abc import ABCMeta, abstractmethod
import itertools

from FibonacciHeap import FibHeap
import heapq


class PriorityQueue():
    __metaclass__ = ABCMeta

    @abstractmethod
    def __len__(self): pass

    @abstractmethod
    def insert(self, priority_item): pass

    @abstractmethod
    def minimum(self): pass

    @abstractmethod
    def removeminimum(self): pass

    @abstractmethod
    def decreasekey(self, item, new_priority): pass

class FibPQ(PriorityQueue):
    def __init__(self):
        self.heap = FibHeap()

    def __len__(self):
        return self.heap.count

    def insert(self, priority_item):
        (priority, item) = priority_item
        node = FibHeap.Node(priority, item)
        self.heap.insert(node)

    def minimum(self):
        return self.heap.minimum().value

    def removeminimum(self):
        self.heap.removeminimum()

    def decreasekey(self, item, new_priority):
        self.heap.decreasekey(item, new_priority)

# Adapted from
# https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
class HeapPQ(PriorityQueue):
    REMOVED_ITEM = '<removed-item>'

    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def __len__(self):
        return len(self.pq)

    def insert(self, priority_item):
        (priority, item) = priority_item
        if item in self.entry_finder:
            self.remove(item)
        entry = [priority, next(self.counter), item]
        self.entry_finder[item] = entry
        heapq.heappush(self.pq, entry)

    def remove(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = REMOVED_ITEM

    def minimum(self):
        [_, _, item] = min(self.pq)
        return item

    def removeminimum(self):
        heapq.heappop(self.pq)

    def decreasekey(self, item, new_priority):
        self.remove(item)
        self.insert((new_priority, item))
