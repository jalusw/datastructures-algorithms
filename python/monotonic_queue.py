import unittest
from collections import deque

class MonotonicQueue:
    """
    MonotonicQueue is a data structure that maintains elements in monotonic order.
    Elements can be efficiently queried for minimum or maximum values in the current window.
    
    Methods:
        - enqueue(value) add value to the queue while maintaining monotonicity
        - dequeue() remove and return the first element
        - peek() return the first element without removing it
        - get_min() return the minimum value in the queue (for non-decreasing mode)
        - get_max() return the maximum value in the queue (for non-increasing mode)
    """
    
    INCREASING = "increasing"  # Min at front (for get_min())
    DECREASING = "decreasing"  # Max at front (for get_max())
    
    def __init__(self, mode=DECREASING):
        """
        Initialize an empty monotonic queue.
        
        Args:
            mode: "increasing" for a non-decreasing queue (supports get_min), 
                 "decreasing" for a non-increasing queue (supports get_max)
        
        Raises:
            ValueError: if mode is not "increasing" or "decreasing"
        """
        if mode not in [self.INCREASING, self.DECREASING]:
            raise ValueError("Mode must be 'increasing' or 'decreasing'")
            
        self.mode = mode
        self.items = deque()  # Main queue for elements
        self.monotonic = deque()  # Monotonic deque for min/max tracking
        self.count = {}  # Count of each value in the queue
        
    def __str__(self) -> str:
        """
        Return the string representation of the queue.
        """
        return f"MonotonicQueue({list(self.items)}, mode={self.mode})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the queue.
        """
        return self.__str__()
        
    def __len__(self) -> int:
        """
        Return the number of elements in the queue.
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
        Add a value to the queue while maintaining monotonicity.
        
        Args:
            value: the value to add
        """
        # Add to the main queue
        self.items.append(value)
        
        # Update count
        if value in self.count:
            self.count[value] += 1
        else:
            self.count[value] = 1
        
        # Update monotonic queue
        if self.mode == self.INCREASING:
            # For min queue (increasing): remove all values greater than the new value
            while self.monotonic and self.monotonic[-1] > value:
                self.monotonic.pop()
        else:
            # For max queue (decreasing): remove all values smaller than the new value
            while self.monotonic and self.monotonic[-1] < value:
                self.monotonic.pop()
                
        self.monotonic.append(value)
        
    def dequeue(self):
        """
        Remove and return the first element.
        
        Returns:
            The first element
            
        Raises:
            IndexError: if the queue is empty
        """
        if not self.items:
            raise IndexError("Cannot dequeue from an empty queue")
            
        value = self.items.popleft()
        
        # Update count
        self.count[value] -= 1
        if self.count[value] == 0:
            del self.count[value]
            
        # Update monotonic queue if needed
        if self.monotonic and self.monotonic[0] == value:
            self.monotonic.popleft()
            
        return value
        
    def peek(self):
        """
        Return the first element without removing it.
        
        Returns:
            The first element
            
        Raises:
            IndexError: if the queue is empty
        """
        if not self.items:
            raise IndexError("Cannot peek at an empty queue")
        return self.items[0]
    
    def get_min(self):
        """
        Return the minimum value in the queue.
        This method is intended for use with mode="increasing".
        
        Returns:
            The minimum value
            
        Raises:
            IndexError: if the queue is empty
            RuntimeError: if the queue is not in "increasing" mode
        """
        if self.mode != self.INCREASING:
            raise RuntimeError("get_min() is only available for 'increasing' mode")
            
        if not self.monotonic:
            raise IndexError("Cannot get minimum from an empty queue")
            
        return self.monotonic[0]
    
    def get_max(self):
        """
        Return the maximum value in the queue.
        This method is intended for use with mode="decreasing".
        
        Returns:
            The maximum value
            
        Raises:
            IndexError: if the queue is empty
            RuntimeError: if the queue is not in "decreasing" mode
        """
        if self.mode != self.DECREASING:
            raise RuntimeError("get_max() is only available for 'decreasing' mode")
            
        if not self.monotonic:
            raise IndexError("Cannot get maximum from an empty queue")
            
        return self.monotonic[0]
    
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Returns:
            True if the queue is empty, False otherwise
        """
        return len(self.items) == 0
    
    def clear(self) -> None:
        """
        Remove all elements from the queue.
        """
        self.items.clear()
        self.monotonic.clear()
        self.count.clear()


class TestMonotonicQueue(unittest.TestCase):
    def setUp(self):
        self.min_queue = MonotonicQueue(mode=MonotonicQueue.INCREASING)
        self.max_queue = MonotonicQueue(mode=MonotonicQueue.DECREASING)
        
    def test_init(self):
        self.assertEqual(len(self.min_queue), 0)
        self.assertEqual(len(self.max_queue), 0)
        self.assertTrue(self.min_queue.is_empty())
        self.assertTrue(self.max_queue.is_empty())
        
        with self.assertRaises(ValueError):
            MonotonicQueue(mode="invalid")
        
    def test_enqueue(self):
        self.min_queue.enqueue(5)
        self.assertEqual(len(self.min_queue), 1)
        self.assertFalse(self.min_queue.is_empty())
        
        self.max_queue.enqueue(5)
        self.assertEqual(len(self.max_queue), 1)
        self.assertFalse(self.max_queue.is_empty())
        
    def test_dequeue(self):
        with self.assertRaises(IndexError):
            self.min_queue.dequeue()
            
        self.min_queue.enqueue(5)
        self.min_queue.enqueue(3)
        
        value = self.min_queue.dequeue()
        self.assertEqual(value, 5)
        self.assertEqual(len(self.min_queue), 1)
        
    def test_peek(self):
        with self.assertRaises(IndexError):
            self.min_queue.peek()
            
        self.min_queue.enqueue(5)
        self.min_queue.enqueue(3)
        
        value = self.min_queue.peek()
        self.assertEqual(value, 5)  # FIFO order
        self.assertEqual(len(self.min_queue), 2)  # Ensure queue is unchanged
        
    def test_min_queue(self):
        # Test increasing (min) queue
        values = [5, 3, 7, 4, 8, 1, 9, 2]
        
        for v in values:
            self.min_queue.enqueue(v)
            
        # Get min should return the current minimum
        self.assertEqual(self.min_queue.get_min(), 1)
        
        # After dequeuing values before the min, min should remain the same
        self.min_queue.dequeue()  # Remove 5
        self.min_queue.dequeue()  # Remove 3
        self.assertEqual(self.min_queue.get_min(), 1)
        
        # After dequeuing the min, the next smallest becomes the min
        while self.min_queue.peek() != 1:
            self.min_queue.dequeue()
        self.min_queue.dequeue()  # Remove 1
        self.assertEqual(self.min_queue.get_min(), 2)
        
    def test_max_queue(self):
        # Test decreasing (max) queue
        values = [5, 8, 3, 9, 7, 2, 6, 1]
        
        for v in values:
            self.max_queue.enqueue(v)
            
        # Get max should return the current maximum
        self.assertEqual(self.max_queue.get_max(), 9)
        
        # After dequeuing values before the max, max should remain the same
        self.max_queue.dequeue()  # Remove 5
        self.max_queue.dequeue()  # Remove 8
        self.assertEqual(self.max_queue.get_max(), 9)
        
        # After dequeuing the max, the next largest becomes the max
        while self.max_queue.peek() != 9:
            self.max_queue.dequeue()
        self.max_queue.dequeue()  # Remove 9
        self.assertEqual(self.max_queue.get_max(), 7)
        
    def test_monotonic_window(self):
        # Test sliding window minimum
        window = MonotonicQueue(mode=MonotonicQueue.INCREASING)
        values = [4, 2, 5, 1, 3, 6, 4, 8]
        window_size = 3
        mins = []
        
        # Process first window
        for i in range(window_size):
            window.enqueue(values[i])
        mins.append(window.get_min())
        
        # Slide window through array
        for i in range(window_size, len(values)):
            window.dequeue()  # Remove oldest element
            window.enqueue(values[i])  # Add new element
            mins.append(window.get_min())
        
        # Expected minimums of each window of size 3
        expected = [2, 1, 1, 1, 3, 4]
        self.assertEqual(mins, expected)
    
    def test_duplicate_values(self):
        # Test with duplicate values
        queue = MonotonicQueue(mode=MonotonicQueue.INCREASING)
        queue.enqueue(3)
        queue.enqueue(1)
        queue.enqueue(1)
        queue.enqueue(2)
        
        self.assertEqual(queue.get_min(), 1)
        
        queue.dequeue()  # Remove 3
        self.assertEqual(queue.get_min(), 1)
        
        queue.dequeue()  # Remove first 1
        self.assertEqual(queue.get_min(), 1)  # Second 1 is still there
        
        queue.dequeue()  # Remove second 1
        self.assertEqual(queue.get_min(), 2)  # Only 2 is left
        
    def test_mode_enforcement(self):
        with self.assertRaises(RuntimeError):
            self.max_queue.get_min()  # Wrong mode
            
        with self.assertRaises(RuntimeError):
            self.min_queue.get_max()  # Wrong mode
            
    def test_contains(self):
        self.min_queue.enqueue(5)
        self.min_queue.enqueue(3)
        
        self.assertTrue(5 in self.min_queue)
        self.assertTrue(3 in self.min_queue)
        self.assertFalse(7 in self.min_queue)
        
    def test_clear(self):
        values = [5, 3, 7, 1]
        for v in values:
            self.min_queue.enqueue(v)
            
        self.assertEqual(len(self.min_queue), 4)
        
        self.min_queue.clear()
        self.assertEqual(len(self.min_queue), 0)
        self.assertTrue(self.min_queue.is_empty())
        
        with self.assertRaises(IndexError):
            self.min_queue.get_min()

if __name__ == '__main__':
    unittest.main()
