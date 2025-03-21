import unittest
from min_heap import MinHeap

class PriorityQueue:
    """
    PriorityQueue is a data structure where each element has a priority.
    Elements with higher priority are served before elements with lower priority.
    
    Methods:
        - enqueue(item, priority) add item with the specified priority
        - dequeue() remove and return the highest priority item
        - peek() return the highest priority item without removing it
    """
    def __init__(self):
        """
        Initialize an empty priority queue.
        """
        self.heap = MinHeap()
        self.entry_count = 0  # To break ties for same priorities
        
    def __str__(self) -> str:
        """
        Return the string representation of the priority queue.
        """
        return f"PriorityQueue({self.heap})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the priority queue.
        """
        return self.__str__()
        
    def __len__(self) -> int:
        """
        Return the number of elements in the priority queue.
        """
        return len(self.heap)
        
    def enqueue(self, item, priority) -> None:
        """
        Add an item with the specified priority.
        
        Args:
            item: the item to add
            priority: the priority of the item (lower number = higher priority)
        """
        # We store (priority, entry_count, item) to ensure stable sorting
        # entry_count is used to break ties for items with the same priority
        entry = (priority, self.entry_count, item)
        self.entry_count += 1
        self.heap.insert(entry)
        
    def dequeue(self):
        """
        Remove and return the highest priority item.
        
        Returns:
            The highest priority item
            
        Raises:
            IndexError: if the priority queue is empty
        """
        if len(self.heap) == 0:
            raise IndexError("Cannot dequeue from an empty priority queue")
            
        priority, _, item = self.heap.extract_min()
        return item
        
    def peek(self):
        """
        Return the highest priority item without removing it.
        
        Returns:
            The highest priority item
            
        Raises:
            IndexError: if the priority queue is empty
        """
        if len(self.heap) == 0:
            raise IndexError("Cannot peek at an empty priority queue")
            
        priority, _, item = self.heap.peek()
        return item
    
    def is_empty(self) -> bool:
        """
        Check if the priority queue is empty.
        
        Returns:
            True if the priority queue is empty, False otherwise
        """
        return self.heap.is_empty()
        
    def clear(self) -> None:
        """
        Remove all elements from the priority queue.
        """
        self.heap.clear()
        self.entry_count = 0


class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.pq = PriorityQueue()
        
    def test_init(self):
        self.assertEqual(len(self.pq), 0)
        self.assertTrue(self.pq.is_empty())
        
    def test_enqueue_dequeue(self):
        # Add items with priorities (lower number = higher priority)
        self.pq.enqueue("Task 1", 3)
        self.pq.enqueue("Task 2", 1)
        self.pq.enqueue("Task 3", 2)
        
        self.assertEqual(len(self.pq), 3)
        
        # Should dequeue in order of priority
        self.assertEqual(self.pq.dequeue(), "Task 2")  # Priority 1
        self.assertEqual(self.pq.dequeue(), "Task 3")  # Priority 2
        self.assertEqual(self.pq.dequeue(), "Task 1")  # Priority 3
        
        self.assertTrue(self.pq.is_empty())
        
    def test_peek(self):
        with self.assertRaises(IndexError):
            self.pq.peek()
            
        self.pq.enqueue("Task 1", 3)
        self.pq.enqueue("Task 2", 1)
        
        self.assertEqual(self.pq.peek(), "Task 2")  # Priority 1
        self.assertEqual(len(self.pq), 2)  # Ensure queue is unchanged
        
    def test_same_priority(self):
        # Items with same priority should be dequeued in the order they were added
        self.pq.enqueue("Task 1", 1)
        self.pq.enqueue("Task 2", 1)
        self.pq.enqueue("Task 3", 1)
        
        self.assertEqual(self.pq.dequeue(), "Task 1")
        self.assertEqual(self.pq.dequeue(), "Task 2")
        self.assertEqual(self.pq.dequeue(), "Task 3")
        
    def test_mixed_priorities(self):
        self.pq.enqueue("Task A", 5)
        self.pq.enqueue("Task B", 2)
        self.pq.enqueue("Task C", 1)
        self.pq.enqueue("Task D", 3)
        self.pq.enqueue("Task E", 1)  # Same priority as C, but added later
        
        self.assertEqual(self.pq.dequeue(), "Task C")  # Priority 1, added first
        self.assertEqual(self.pq.dequeue(), "Task E")  # Priority 1, added second
        self.assertEqual(self.pq.dequeue(), "Task B")  # Priority 2
        self.assertEqual(self.pq.dequeue(), "Task D")  # Priority 3
        self.assertEqual(self.pq.dequeue(), "Task A")  # Priority 5
        
    def test_clear(self):
        for i in range(5):
            self.pq.enqueue(f"Task {i}", i)
            
        self.assertEqual(len(self.pq), 5)
        
        self.pq.clear()
        self.assertEqual(len(self.pq), 0)
        self.assertTrue(self.pq.is_empty())

if __name__ == '__main__':
    unittest.main()
