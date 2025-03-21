import unittest

class Queue:
    """
    Queue is a FIFO (first-in, first-out) data structure.
    
    Methods:
        - enqueue(value) add value to the end of the queue
        - dequeue() remove and return the first element
        - peek() return the first element without removing it
    """
    def __init__(self):
        """
        Initialize an empty queue.
        """
        self.items = []
        
    def __str__(self) -> str:
        """
        Return the string representation of the queue.
        """
        return f"{self.items}"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the queue.
        """
        return f"Queue({self.items})"
        
    def __len__(self) -> int:
        """
        Return the length of the queue.
        """
        return len(self.items)
        
    def __contains__(self, value) -> bool:
        """
        Check if the value is in the queue.
        
        Args:
            value: the value to check
        """
        return value in self.items
        
    def enqueue(self, value) -> None:
        """
        Add value to the end of the queue.
        
        Args:
            value: the value to add
        """
        self.items.append(value)
        
    def dequeue(self):
        """
        Remove and return the first element.
        
        Returns:
            The first element
            
        Raises:
            IndexError: if the queue is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot dequeue from an empty queue")
        return self.items.pop(0)
        
    def peek(self):
        """
        Return the first element without removing it.
        
        Returns:
            The first element
            
        Raises:
            IndexError: if the queue is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot peek at an empty queue")
        return self.items[0]
        
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Returns:
            True if the queue is empty, False otherwise
        """
        return len(self.items) == 0


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
        
    def test_init(self):
        self.assertEqual(self.queue.items, [])
        self.assertEqual(len(self.queue), 0)
        self.assertTrue(self.queue.is_empty())
        
    def test_enqueue(self):
        self.queue.enqueue(1)
        self.assertEqual(self.queue.items, [1])
        self.assertEqual(len(self.queue), 1)
        self.assertFalse(self.queue.is_empty())
        
        self.queue.enqueue(2)
        self.assertEqual(self.queue.items, [1, 2])
        self.assertEqual(len(self.queue), 2)
        
    def test_dequeue(self):
        with self.assertRaises(IndexError):
            self.queue.dequeue()
            
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        
        value = self.queue.dequeue()
        self.assertEqual(value, 1)
        self.assertEqual(self.queue.items, [2])
        self.assertEqual(len(self.queue), 1)
        
    def test_peek(self):
        with self.assertRaises(IndexError):
            self.queue.peek()
            
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        
        value = self.queue.peek()
        self.assertEqual(value, 1)
        self.assertEqual(self.queue.items, [1, 2])  # Ensure queue is unchanged
        self.assertEqual(len(self.queue), 2)
        
    def test_contains(self):
        self.queue.enqueue(1)
        self.queue.enqueue(3)
        self.assertFalse(2 in self.queue)
        self.assertTrue(1 in self.queue)
        
    def test_fifo_order(self):
        for i in range(5):
            self.queue.enqueue(i)
            
        for i in range(5):
            self.assertEqual(self.queue.dequeue(), i)
            
        self.assertTrue(self.queue.is_empty())

if __name__ == '__main__':
    unittest.main()
