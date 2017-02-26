
from abc import ABCMeta, abstractmethod
import itertools

from FibonacciHeap import FibHeap
import heapq
import Queue

class PriorityQueue():
    __metaclass__ = ABCMeta

    @abstractmethod
    def __len__(self): pass

    @abstractmethod
    def insert(self, node): pass

    @abstractmethod
    def minimum(self): pass

    @abstractmethod
    def removeminimum(self): pass

    @abstractmethod
    def decreasekey(self, node, new_priority): pass

class FibPQ(PriorityQueue):
    def __init__(self):
        self.heap = FibHeap()

    def __len__(self):
        return self.heap.count

    def insert(self, node):
        self.heap.insert(node)

    def minimum(self):
        return self.heap.minimum()

    def removeminimum(self):
        return self.heap.removeminimum()

    def decreasekey(self, node, new_priority):
        self.heap.decreasekey(node, new_priority)

class HeapPQ(PriorityQueue):
    def __init__(self):
        self.pq = []
        self.removed = set()
        self.count = 0

    def __len__(self):
        return self.count

    def insert(self, node):
        entry = node.key, node.value
        if entry in self.removed:
            self.removed.discard(entry)
        heapq.heappush(self.pq, entry)
        self.count += 1

    def minimum(self):
        priority, item = heapq.heappop(self.pq)
        node = FibHeap.Node(priority, item)
        self.insert(node)
        return node

    def removeminimum(self):
        while True:
            (priority, item) = heapq.heappop(self.pq)
            if (priority, item) in self.removed:
                self.removed.discard((priority, item))
            else:
                self.count -= 1
                return FibHeap.Node(priority, item)

    def remove(self, node):
        entry = node.key, node.value
        if entry not in self.removed:
            self.removed.add(entry)
            self.count -= 1

    def decreasekey(self, node, new_priority):
        self.remove(node)
        node.key = new_priority
        self.insert(node)


class QueuePQ(PriorityQueue):
    def __init__(self):
        self.pq = Queue.PriorityQueue()
        self.removed = set()
        self.count = 0

    def __len__(self):
        return self.count

    def insert(self, node):
        entry = node.key, node.value
        if entry in self.removed:
            self.removed.discard(entry)
        self.pq.put(entry)
        self.count += 1

    def minimum(self):
        (priority, item) = self.pq.get_nowait()
        node = FibHeap.Node(priority, item)
        self.insert(node)
        return node

    def removeminimum(self):
        while True:
            (priority, item) = self.pq.get_nowait()
            if (priority, item) in self.removed:
                self.removed.discard((priority, item))
            else:
                self.count -= 1
                return FibHeap.Node(priority, item)

    def remove(self, node):
        entry = node.key, node.value
        if entry not in self.removed:
            self.removed.add(entry)
            self.count -= 1

    def decreasekey(self, node, new_priority):
        self.remove(node)
        node.key = new_priority
        self.insert(node)

