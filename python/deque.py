import unittest

class Deque:
    """
    Deque (double-ended queue) is a data structure that allows insertion and removal
    at both the front and back.
    
    Methods:
        - append(value) add value to the end of the deque
        - appendleft(value) add value to the beginning of the deque
        - pop() remove and return the last element
        - popleft() remove and return the first element
        - peek() return the last element without removing it
        - peekleft() return the first element without removing it
    """
    def __init__(self):
        """
        Initialize an empty deque.
        """
        self.items = []
        
    def __str__(self) -> str:
        """
        Return the string representation of the deque.
        """
        return f"{self.items}"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the deque.
        """
        return f"Deque({self.items})"
        
    def __len__(self) -> int:
        """
        Return the length of the deque.
        """
        return len(self.items)
        
    def __contains__(self, value) -> bool:
        """
        Check if the value is in the deque.
        
        Args:
            value: the value to check
        """
        return value in self.items
    
    def __getitem__(self, index):
        """
        Return the value at the specified index.

        Args:
            index: the index of the value to return

        Raises:
            IndexError: if the index is out of range
        """
        if index >= len(self.items) or index < -len(self.items):
            raise IndexError("Index out of range")
        return self.items[index]
        
    def append(self, value) -> None:
        """
        Add value to the end of the deque.
        
        Args:
            value: the value to add
        """
        self.items.append(value)
    
    def appendleft(self, value) -> None:
        """
        Add value to the beginning of the deque.
        
        Args:
            value: the value to add
        """
        self.items.insert(0, value)
        
    def pop(self):
        """
        Remove and return the last element.
        
        Returns:
            The last element
            
        Raises:
            IndexError: if the deque is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot pop from an empty deque")
        return self.items.pop()
    
    def popleft(self):
        """
        Remove and return the first element.
        
        Returns:
            The first element
            
        Raises:
            IndexError: if the deque is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot popleft from an empty deque")
        return self.items.pop(0)
        
    def peek(self):
        """
        Return the last element without removing it.
        
        Returns:
            The last element
            
        Raises:
            IndexError: if the deque is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot peek at an empty deque")
        return self.items[-1]
    
    def peekleft(self):
        """
        Return the first element without removing it.
        
        Returns:
            The first element
            
        Raises:
            IndexError: if the deque is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot peekleft at an empty deque")
        return self.items[0]
        
    def is_empty(self) -> bool:
        """
        Check if the deque is empty.
        
        Returns:
            True if the deque is empty, False otherwise
        """
        return len(self.items) == 0
    
    def clear(self) -> None:
        """
        Remove all elements from the deque.
        """
        self.items = []


class TestDeque(unittest.TestCase):
    def setUp(self):
        self.deque = Deque()
        
    def test_init(self):
        self.assertEqual(self.deque.items, [])
        self.assertEqual(len(self.deque), 0)
        self.assertTrue(self.deque.is_empty())
        
    def test_append(self):
        self.deque.append(1)
        self.assertEqual(self.deque.items, [1])
        self.assertEqual(len(self.deque), 1)
        self.assertFalse(self.deque.is_empty())
        
        self.deque.append(2)
        self.assertEqual(self.deque.items, [1, 2])
        self.assertEqual(len(self.deque), 2)
    
    def test_appendleft(self):
        self.deque.appendleft(1)
        self.assertEqual(self.deque.items, [1])
        self.assertEqual(len(self.deque), 1)
        
        self.deque.appendleft(2)
        self.assertEqual(self.deque.items, [2, 1])
        self.assertEqual(len(self.deque), 2)
        
    def test_pop(self):
        with self.assertRaises(IndexError):
            self.deque.pop()
            
        self.deque.append(1)
        self.deque.append(2)
        
        value = self.deque.pop()
        self.assertEqual(value, 2)
        self.assertEqual(self.deque.items, [1])
        self.assertEqual(len(self.deque), 1)
    
    def test_popleft(self):
        with self.assertRaises(IndexError):
            self.deque.popleft()
            
        self.deque.append(1)
        self.deque.append(2)
        
        value = self.deque.popleft()
        self.assertEqual(value, 1)
        self.assertEqual(self.deque.items, [2])
        self.assertEqual(len(self.deque), 1)
        
    def test_peek(self):
        with self.assertRaises(IndexError):
            self.deque.peek()
            
        self.deque.append(1)
        self.deque.append(2)
        
        value = self.deque.peek()
        self.assertEqual(value, 2)
        self.assertEqual(self.deque.items, [1, 2])  # Ensure deque is unchanged
        self.assertEqual(len(self.deque), 2)
    
    def test_peekleft(self):
        with self.assertRaises(IndexError):
            self.deque.peekleft()
            
        self.deque.append(1)
        self.deque.append(2)
        
        value = self.deque.peekleft()
        self.assertEqual(value, 1)
        self.assertEqual(self.deque.items, [1, 2])  # Ensure deque is unchanged
        self.assertEqual(len(self.deque), 2)
        
    def test_contains(self):
        self.deque.append(1)
        self.deque.append(3)
        self.assertFalse(2 in self.deque)
        self.assertTrue(1 in self.deque)
    
    def test_getitem(self):
        self.deque.append(10)
        self.deque.append(20)
        
        self.assertEqual(self.deque[0], 10)
        self.assertEqual(self.deque[1], 20)
        self.assertEqual(self.deque[-1], 20)
        self.assertEqual(self.deque[-2], 10)
        
        with self.assertRaises(IndexError):
            self.deque[2]
        
        with self.assertRaises(IndexError):
            self.deque[-3]
    
    def test_clear(self):
        self.deque.append(1)
        self.deque.append(2)
        self.assertEqual(len(self.deque), 2)
        
        self.deque.clear()
        self.assertEqual(len(self.deque), 0)
        self.assertTrue(self.deque.is_empty())
        
    def test_mixed_operations(self):
        # Test a mix of operations from both ends
        self.deque.append(1)      # [1]
        self.deque.appendleft(2)  # [2, 1]
        self.deque.append(3)      # [2, 1, 3]
        
        self.assertEqual(self.deque.pop(), 3)     # [2, 1]
        self.assertEqual(self.deque.popleft(), 2) # [1]
        
        self.deque.appendleft(4)  # [4, 1]
        self.deque.append(5)      # [4, 1, 5]
        
        self.assertEqual(self.deque.items, [4, 1, 5])
        self.assertEqual(self.deque.peek(), 5)
        self.assertEqual(self.deque.peekleft(), 4)

if __name__ == '__main__':
    unittest.main()
