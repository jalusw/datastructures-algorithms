import unittest
from typing import Any, Callable, List, Optional, Union

class SegmentTree:
    """
    A Segment Tree is a data structure that efficiently supports range queries
    and point updates. It can be used for various operations like:
    - Range sum queries
    - Range minimum/maximum queries
    - Range GCD queries
    - Range XOR queries
    - And other associative operations
    
    The tree is implemented using a binary tree structure, where each node
    represents a segment of the array. The root node represents the entire array,
    and each child node represents half of its parent's segment.
    
    Methods:
        - update(index, value) update a single element
        - query(start, end) get result of operation on range [start, end]
        - get(index) get value at index
        - set(index, value) set value at index
    """
    def __init__(self, size: int, operation: Callable[[Any, Any], Any], initial_values: Optional[List[Any]] = None):
        """
        Initialize a Segment Tree with the given size and operation.
        
        Args:
            size: The size of the array
            operation: The operation to perform (e.g., sum, min, max)
            initial_values: Optional list of initial values
        """
        self.size = size
        self.operation = operation
        
        # Calculate tree size (next power of 2)
        self.tree_size = 2 * (1 << (size - 1).bit_length()) - 1
        self.tree = [None] * self.tree_size
        
        if initial_values:
            if len(initial_values) != size:
                raise ValueError("Initial values length must match size")
            self._build(0, 0, size - 1, initial_values)
            
    def __str__(self) -> str:
        """
        Return the string representation of the Segment Tree.
        """
        return f"SegmentTree(size={self.size}, operation={self.operation.__name__})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the Segment Tree.
        """
        return self.__str__()
        
    def _build(self, node: int, start: int, end: int, values: List[Any]) -> None:
        """
        Build the segment tree recursively.
        
        Args:
            node: The current node index
            start: The start index of the segment
            end: The end index of the segment
            values: The array of values
        """
        if start == end:
            self.tree[node] = values[start]
            return
            
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        self._build(left_child, start, mid, values)
        self._build(right_child, mid + 1, end, values)
        
        self.tree[node] = self.operation(self.tree[left_child], self.tree[right_child])
        
    def _update(self, node: int, start: int, end: int, index: int, value: Any) -> None:
        """
        Update a single element recursively.
        
        Args:
            node: The current node index
            start: The start index of the segment
            end: The end index of the segment
            index: The index to update
            value: The new value
        """
        if start == end:
            self.tree[node] = value
            return
            
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        if index <= mid:
            self._update(left_child, start, mid, index, value)
        else:
            self._update(right_child, mid + 1, end, index, value)
            
        self.tree[node] = self.operation(self.tree[left_child], self.tree[right_child])
        
    def _query(self, node: int, start: int, end: int, left: int, right: int) -> Any:
        """
        Query a range recursively.
        
        Args:
            node: The current node index
            start: The start index of the segment
            end: The end index of the segment
            left: The left index of the query range
            right: The right index of the query range
            
        Returns:
            The result of the operation on the range
        """
        if right < start or left > end:
            return None
            
        if left <= start and right >= end:
            return self.tree[node]
            
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_result = self._query(left_child, start, mid, left, right)
        right_result = self._query(right_child, mid + 1, end, left, right)
        
        if left_result is None:
            return right_result
        if right_result is None:
            return left_result
            
        return self.operation(left_result, right_result)
        
    def update(self, index: int, value: Any) -> None:
        """
        Update a single element.
        
        Args:
            index: The index to update (0-based)
            value: The new value
        """
        if not 0 <= index < self.size:
            raise IndexError("Index out of range")
            
        self._update(0, 0, self.size - 1, index, value)
        
    def query(self, start: int, end: int) -> Any:
        """
        Get the result of the operation on the range [start, end].
        
        Args:
            start: The start index (inclusive)
            end: The end index (inclusive)
            
        Returns:
            The result of the operation
        """
        if not 0 <= start <= end < self.size:
            raise IndexError("Index out of range")
            
        return self._query(0, 0, self.size - 1, start, end)
        
    def get(self, index: int) -> Any:
        """
        Get the value at the given index.
        
        Args:
            index: The index to get the value from (0-based)
            
        Returns:
            The value at the index
        """
        if not 0 <= index < self.size:
            raise IndexError("Index out of range")
            
        return self.query(index, index)
        
    def set(self, index: int, value: Any) -> None:
        """
        Set the value at the given index.
        
        Args:
            index: The index to set the value at (0-based)
            value: The value to set
        """
        if not 0 <= index < self.size:
            raise IndexError("Index out of range")
            
        self.update(index, value)
        
    def clear(self) -> None:
        """
        Clear all values in the tree.
        """
        self.tree = [None] * self.tree_size


class TestSegmentTree(unittest.TestCase):
    def setUp(self):
        # Create segment trees for different operations
        self.sum_tree = SegmentTree(5, lambda x, y: x + y if x is not None and y is not None else x if x is not None else y)
        self.min_tree = SegmentTree(5, lambda x, y: min(x, y) if x is not None and y is not None else x if x is not None else y)
        self.max_tree = SegmentTree(5, lambda x, y: max(x, y) if x is not None and y is not None else x if x is not None else y)
        
    def test_init(self):
        self.assertEqual(self.sum_tree.size, 5)
        self.assertEqual(self.min_tree.size, 5)
        self.assertEqual(self.max_tree.size, 5)
        
        # Test initialization with values
        values = [1, 2, 3, 4, 5]
        st = SegmentTree(5, lambda x, y: x + y if x is not None and y is not None else x if x is not None else y, values)
        self.assertEqual(st.query(0, 4), 15)
        
    def test_update(self):
        # Test sum tree
        self.sum_tree.update(0, 1)
        self.sum_tree.update(1, 2)
        self.sum_tree.update(2, 3)
        self.assertEqual(self.sum_tree.query(0, 2), 6)
        
        # Test min tree
        self.min_tree.update(0, 3)
        self.min_tree.update(1, 1)
        self.min_tree.update(2, 2)
        self.assertEqual(self.min_tree.query(0, 2), 1)
        
        # Test max tree
        self.max_tree.update(0, 1)
        self.max_tree.update(1, 3)
        self.max_tree.update(2, 2)
        self.assertEqual(self.max_tree.query(0, 2), 3)
        
    def test_query(self):
        # Set up values
        values = [1, 2, 3, 4, 5]
        for i, value in enumerate(values):
            self.sum_tree.update(i, value)
            self.min_tree.update(i, value)
            self.max_tree.update(i, value)
            
        # Test sum queries
        self.assertEqual(self.sum_tree.query(0, 0), 1)
        self.assertEqual(self.sum_tree.query(0, 1), 3)
        self.assertEqual(self.sum_tree.query(1, 2), 5)
        self.assertEqual(self.sum_tree.query(2, 4), 12)
        self.assertEqual(self.sum_tree.query(0, 4), 15)
        
        # Test min queries
        self.assertEqual(self.min_tree.query(0, 0), 1)
        self.assertEqual(self.min_tree.query(0, 1), 1)
        self.assertEqual(self.min_tree.query(1, 2), 2)
        self.assertEqual(self.min_tree.query(2, 4), 3)
        self.assertEqual(self.min_tree.query(0, 4), 1)
        
        # Test max queries
        self.assertEqual(self.max_tree.query(0, 0), 1)
        self.assertEqual(self.max_tree.query(0, 1), 2)
        self.assertEqual(self.max_tree.query(1, 2), 3)
        self.assertEqual(self.max_tree.query(2, 4), 5)
        self.assertEqual(self.max_tree.query(0, 4), 5)
        
    def test_get(self):
        # Set up values
        values = [1, 2, 3, 4, 5]
        for i, value in enumerate(values):
            self.sum_tree.update(i, value)
            
        # Test getting individual values
        self.assertEqual(self.sum_tree.get(0), 1)
        self.assertEqual(self.sum_tree.get(1), 2)
        self.assertEqual(self.sum_tree.get(2), 3)
        self.assertEqual(self.sum_tree.get(3), 4)
        self.assertEqual(self.sum_tree.get(4), 5)
        
    def test_set(self):
        # Set up values
        self.sum_tree.update(0, 1)
        self.sum_tree.update(1, 2)
        self.sum_tree.update(2, 3)
        
        # Test setting values
        self.sum_tree.set(1, 5)
        self.assertEqual(self.sum_tree.get(1), 5)
        self.assertEqual(self.sum_tree.query(0, 2), 9)
        
        self.sum_tree.set(2, 7)
        self.assertEqual(self.sum_tree.get(2), 7)
        self.assertEqual(self.sum_tree.query(0, 2), 13)
        
    def test_clear(self):
        # Set up values
        self.sum_tree.update(0, 1)
        self.sum_tree.update(1, 2)
        self.sum_tree.update(2, 3)
        
        # Clear the tree
        self.sum_tree.clear()
        
        # Verify all values are None
        self.assertIsNone(self.sum_tree.query(0, 4))
        self.assertIsNone(self.sum_tree.get(0))
        self.assertIsNone(self.sum_tree.get(1))
        self.assertIsNone(self.sum_tree.get(2))
        
    def test_edge_cases(self):
        # Test empty range
        self.assertIsNone(self.sum_tree.query(0, 0))
        
        # Test full range
        self.sum_tree.update(0, 1)
        self.sum_tree.update(1, 2)
        self.sum_tree.update(2, 3)
        self.sum_tree.update(3, 4)
        self.sum_tree.update(4, 5)
        self.assertEqual(self.sum_tree.query(0, 4), 15)
        
        # Test single element
        self.assertEqual(self.sum_tree.get(2), 3)
        
    def test_error_handling(self):
        # Test out of range indices
        with self.assertRaises(IndexError):
            self.sum_tree.update(-1, 1)
        with self.assertRaises(IndexError):
            self.sum_tree.update(5, 1)
        with self.assertRaises(IndexError):
            self.sum_tree.query(-1, 0)
        with self.assertRaises(IndexError):
            self.sum_tree.query(0, 5)
        with self.assertRaises(IndexError):
            self.sum_tree.get(-1)
        with self.assertRaises(IndexError):
            self.sum_tree.get(5)
        with self.assertRaises(IndexError):
            self.sum_tree.set(-1, 1)
        with self.assertRaises(IndexError):
            self.sum_tree.set(5, 1)
            
    def test_complex_operations(self):
        # Create a larger tree
        st = SegmentTree(10, lambda x, y: x + y if x is not None and y is not None else x if x is not None else y)
        
        # Perform multiple updates
        for i in range(10):
            st.update(i, i + 1)
            
        # Test various range queries
        self.assertEqual(st.query(0, 9), 55)
        self.assertEqual(st.query(2, 5), 18)
        self.assertEqual(st.query(7, 9), 24)
        
        # Test setting values
        st.set(3, 10)
        self.assertEqual(st.get(3), 10)
        self.assertEqual(st.query(0, 3), 16)
        
        # Test multiple updates to same index
        st.update(5, 5)
        st.update(5, -2)
        self.assertEqual(st.get(5), 9)
        
        # Test prefix sums
        self.assertEqual(st.query(0, 4), 15)
        self.assertEqual(st.query(0, 7), 34)
        self.assertEqual(st.query(0, 9), 58)
        
    def test_different_operations(self):
        # Test GCD operation
        gcd_tree = SegmentTree(5, lambda x, y: self._gcd(x, y) if x is not None and y is not None else x if x is not None else y)
        values = [12, 18, 24, 36, 48]
        for i, value in enumerate(values):
            gcd_tree.update(i, value)
        self.assertEqual(gcd_tree.query(0, 4), 6)
        
        # Test XOR operation
        xor_tree = SegmentTree(5, lambda x, y: x ^ y if x is not None and y is not None else x if x is not None else y)
        values = [1, 2, 3, 4, 5]
        for i, value in enumerate(values):
            xor_tree.update(i, value)
        self.assertEqual(xor_tree.query(0, 4), 1)
        
    def _gcd(self, a: int, b: int) -> int:
        """
        Calculate the greatest common divisor of two numbers.
        """
        while b:
            a, b = b, a % b
        return a


if __name__ == '__main__':
    unittest.main() 