
from abc import ABCMeta, abstractmethod
from FibonacciHeap import FibHeap

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
        return self.heap.minimum()

    def removeminimum(self):
        self.heap.removeminimum()

    def decreasekey(self, item, new_priority):
        self.heap.decreasekey(item, new_priority)
