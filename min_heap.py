import unittest

class MinHeap:
    """
    MinHeap is a complete binary tree where the value at each node is smaller than
    or equal to the values in its children nodes.
    
    Methods:
        - insert(value) add value to the heap
        - extract_min() remove and return the minimum value
        - peek() return the minimum value without removing it
    """
    def __init__(self):
        """
        Initialize an empty min heap.
        """
        self.items = []
        
    def __str__(self) -> str:
        """
        Return the string representation of the heap.
        """
        return f"{self.items}"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the heap.
        """
        return f"MinHeap({self.items})"
        
    def __len__(self) -> int:
        """
        Return the number of elements in the heap.
        """
        return len(self.items)
        
    def __contains__(self, value) -> bool:
        """
        Check if the value is in the heap.
        
        Args:
            value: the value to check
        """
        return value in self.items
    
    def _parent_index(self, index):
        """
        Get the parent index of the element at the specified index.
        
        Args:
            index: the index of the element
            
        Returns:
            The parent index or None if the element is the root
        """
        if index <= 0:
            return None
        return (index - 1) // 2
        
    def _left_child_index(self, index):
        """
        Get the left child index of the element at the specified index.
        
        Args:
            index: the index of the element
            
        Returns:
            The left child index or None if there is no left child
        """
        left = 2 * index + 1
        if left >= len(self.items):
            return None
        return left
        
    def _right_child_index(self, index):
        """
        Get the right child index of the element at the specified index.
        
        Args:
            index: the index of the element
            
        Returns:
            The right child index or None if there is no right child
        """
        right = 2 * index + 2
        if right >= len(self.items):
            return None
        return right
        
    def _sift_up(self, index):
        """
        Move the element at the specified index up the heap until the heap property is restored.
        
        Args:
            index: the index of the element to sift up
        """
        parent = self._parent_index(index)
        
        if parent is not None and self.items[index] < self.items[parent]:
            # Swap with parent
            self.items[index], self.items[parent] = self.items[parent], self.items[index]
            # Continue sifting up
            self._sift_up(parent)
    
    def _sift_down(self, index):
        """
        Move the element at the specified index down the heap until the heap property is restored.
        
        Args:
            index: the index of the element to sift down
        """
        smallest = index
        left = self._left_child_index(index)
        right = self._right_child_index(index)
        
        if left is not None and self.items[left] < self.items[smallest]:
            smallest = left
            
        if right is not None and self.items[right] < self.items[smallest]:
            smallest = right
            
        if smallest != index:
            # Swap with the smallest child
            self.items[index], self.items[smallest] = self.items[smallest], self.items[index]
            # Continue sifting down
            self._sift_down(smallest)
    
    def insert(self, value) -> None:
        """
        Insert a value into the heap.
        
        Args:
            value: the value to insert
        """
        self.items.append(value)
        self._sift_up(len(self.items) - 1)
        
    def extract_min(self):
        """
        Remove and return the minimum value from the heap.
        
        Returns:
            The minimum value
            
        Raises:
            IndexError: if the heap is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot extract from an empty heap")
            
        min_value = self.items[0]
        
        # Move the last item to the root
        self.items[0] = self.items[-1]
        self.items.pop()
        
        # Restore the heap property
        if len(self.items) > 0:
            self._sift_down(0)
            
        return min_value
        
    def peek(self):
        """
        Return the minimum value without removing it.
        
        Returns:
            The minimum value
            
        Raises:
            IndexError: if the heap is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot peek at an empty heap")
        return self.items[0]
    
    def is_empty(self) -> bool:
        """
        Check if the heap is empty.
        
        Returns:
            True if the heap is empty, False otherwise
        """
        return len(self.items) == 0
        
    def clear(self) -> None:
        """
        Remove all elements from the heap.
        """
        self.items = []


class TestMinHeap(unittest.TestCase):
    def setUp(self):
        self.heap = MinHeap()
        
    def test_init(self):
        self.assertEqual(self.heap.items, [])
        self.assertEqual(len(self.heap), 0)
        self.assertTrue(self.heap.is_empty())
        
    def test_insert(self):
        self.heap.insert(5)
        self.assertEqual(self.heap.items, [5])
        
        self.heap.insert(3)
        self.assertEqual(len(self.heap), 2)
        self.assertEqual(self.heap.items[0], 3)  # 3 should be at root
        
        self.heap.insert(7)
        self.assertEqual(len(self.heap), 3)
        self.assertEqual(self.heap.items[0], 3)  # 3 should still be at root
        
        self.heap.insert(1)
        self.assertEqual(len(self.heap), 4)
        self.assertEqual(self.heap.items[0], 1)  # 1 should be at root
        
    def test_extract_min(self):
        with self.assertRaises(IndexError):
            self.heap.extract_min()
            
        # Insert in arbitrary order
        values = [5, 3, 7, 1, 8, 2, 4]
        for v in values:
            self.heap.insert(v)
            
        # Extract in ascending order
        self.assertEqual(self.heap.extract_min(), 1)
        self.assertEqual(self.heap.extract_min(), 2)
        self.assertEqual(self.heap.extract_min(), 3)
        self.assertEqual(self.heap.extract_min(), 4)
        self.assertEqual(self.heap.extract_min(), 5)
        self.assertEqual(self.heap.extract_min(), 7)
        self.assertEqual(self.heap.extract_min(), 8)
        
        self.assertTrue(self.heap.is_empty())
        
    def test_peek(self):
        with self.assertRaises(IndexError):
            self.heap.peek()
            
        self.heap.insert(5)
        self.heap.insert(3)
        
        self.assertEqual(self.heap.peek(), 3)
        self.assertEqual(len(self.heap), 2)  # Ensure heap is unchanged
        
        self.heap.insert(1)
        self.assertEqual(self.heap.peek(), 1)
        
    def test_contains(self):
        self.heap.insert(5)
        self.heap.insert(3)
        self.heap.insert(7)
        
        self.assertTrue(5 in self.heap)
        self.assertTrue(3 in self.heap)
        self.assertTrue(7 in self.heap)
        self.assertFalse(10 in self.heap)
        
    def test_heap_property(self):
        values = [9, 5, 7, 1, 3, 8, 2, 4, 6]
        for v in values:
            self.heap.insert(v)
            
        # Check that each parent is less than or equal to its children
        for i in range(len(self.heap.items)):
            left = self.heap._left_child_index(i)
            right = self.heap._right_child_index(i)
            
            if left is not None:
                self.assertLessEqual(self.heap.items[i], self.heap.items[left])
                
            if right is not None:
                self.assertLessEqual(self.heap.items[i], self.heap.items[right])
        
    def test_clear(self):
        for i in range(5):
            self.heap.insert(i)
            
        self.assertEqual(len(self.heap), 5)
        
        self.heap.clear()
        self.assertEqual(len(self.heap), 0)
        self.assertTrue(self.heap.is_empty())

if __name__ == '__main__':
    unittest.main()
