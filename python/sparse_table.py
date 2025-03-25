import unittest
import math
from typing import List, Callable, TypeVar, Generic, Optional, Union, Tuple

T = TypeVar('T')

class SparseTable(Generic[T]):
    """
    SparseTable is a data structure for efficient range queries on static arrays.
    
    It supports O(1) queries for idempotent operations like min, max, gcd, and
    O(log n) queries for non-idempotent operations like sum.
    
    Methods:
        - query(left, right) perform a query on the range [left, right]
        - query_idempotent(left, right) perform a query using O(1) method for idempotent operations
        - query_non_idempotent(left, right) perform a query using O(log n) method for non-idempotent operations
    """
    def __init__(self, array: List[T], operation: Callable[[T, T], T], idempotent: bool = True):
        """
        Initialize a sparse table with the given array and operation.
        
        Args:
            array: The input array
            operation: The binary function to use for range queries (e.g., min, max, gcd)
            idempotent: Whether the operation is idempotent (e.g., min, max, gcd)
                        If True, uses O(1) query method; if False, uses O(log n) query method
        """
        self.array = array.copy()
        self.operation = operation
        self.idempotent = idempotent
        self.n = len(array)
        
        # Calculate log2(n) to determine table height
        if self.n > 0:
            self.log_n = math.floor(math.log2(self.n)) + 1
        else:
            self.log_n = 1
            
        # Initialize sparse table
        self.table = self._build_table()
        
    def __str__(self) -> str:
        """
        Return the string representation of the sparse table.
        """
        return f"SparseTable({self.array})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the sparse table.
        """
        return self.__str__()
        
    def __len__(self) -> int:
        """
        Return the length of the underlying array.
        """
        return self.n
        
    def _build_table(self) -> List[List[T]]:
        """
        Build the sparse table.
        
        Returns:
            A 2D array representing the sparse table
        """
        if self.n == 0:
            return [[]]
            
        # Initialize table with dimensions [log_n][n]
        table = [[None for _ in range(self.n)] for _ in range(self.log_n)]
        
        # Base case: The interval of length 1 is just the array itself
        for i in range(self.n):
            table[0][i] = self.array[i]
            
        # Fill the rest of the table using dynamic programming
        for k in range(1, self.log_n):
            # Length of the current interval
            length = 1 << k
            # Previous length
            prev_length = 1 << (k-1)
            
            for i in range(self.n - length + 1):
                # Combine two intervals of length 2^(k-1)
                table[k][i] = self.operation(
                    table[k-1][i],
                    table[k-1][i + prev_length]
                )
                
        return table
                
    def query(self, left: int, right: int) -> T:
        """
        Perform a range query on the interval [left, right].
        Uses the appropriate query method based on whether the operation is idempotent.
        
        Args:
            left: The start index (inclusive)
            right: The end index (inclusive)
            
        Returns:
            The result of the operation on the range
            
        Raises:
            IndexError: If the range is invalid
            ValueError: If the array is empty
        """
        self._validate_range(left, right)
        
        if self.idempotent:
            return self.query_idempotent(left, right)
        else:
            return self.query_non_idempotent(left, right)
            
    def query_idempotent(self, left: int, right: int) -> T:
        """
        Perform a range query for idempotent operations (min, max, gcd, etc.) in O(1) time.
        
        Args:
            left: The start index (inclusive)
            right: The end index (inclusive)
            
        Returns:
            The result of the operation on the range
            
        Raises:
            IndexError: If the range is invalid
            ValueError: If the array is empty
        """
        self._validate_range(left, right)
        
        # Special case: single element
        if left == right:
            return self.array[left]
            
        # Length of the range
        length = right - left + 1
        # Largest power of 2 <= length
        k = math.floor(math.log2(length))
        
        # For idempotent operations, we can overlap the intervals
        # First interval: [left, left + 2^k - 1]
        # Second interval: [right - 2^k + 1, right]
        return self.operation(
            self.table[k][left],
            self.table[k][right - (1 << k) + 1]
        )
        
    def query_non_idempotent(self, left: int, right: int) -> T:
        """
        Perform a range query for non-idempotent operations (sum, product, etc.) in O(log n) time.
        
        Args:
            left: The start index (inclusive)
            right: The end index (inclusive)
            
        Returns:
            The result of the operation on the range
            
        Raises:
            IndexError: If the range is invalid
            ValueError: If the array is empty
        """
        self._validate_range(left, right)
        
        # Special case: single element
        if left == right:
            return self.array[left]
            
        # We need to divide the range into non-overlapping powers of 2
        result = None
        p = 0  # Current power of 2
        
        while left <= right:
            # Find largest k such that 2^k <= (right - left + 1)
            k = 0
            while (1 << (k + 1)) <= (right - left + 1):
                k += 1
                
            # Apply operation with the current interval
            interval_value = self.table[k][left]
            if result is None:
                result = interval_value
            else:
                result = self.operation(result, interval_value)
                
            # Move to the next interval
            left += (1 << k)
            
        return result
    
    def _validate_range(self, left: int, right: int) -> None:
        """
        Validate that the query range is valid.
        
        Args:
            left: The start index
            right: The end index
            
        Raises:
            IndexError: If the range is invalid
            ValueError: If the array is empty
        """
        if self.n == 0:
            raise ValueError("Cannot query an empty array")
            
        if left < 0 or right >= self.n or left > right:
            raise IndexError(f"Invalid range [{left}, {right}]")


class TestSparseTable(unittest.TestCase):
    def setUp(self):
        # Create sparse tables for different operations
        self.min_array = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        self.min_table = SparseTable(self.min_array, min, idempotent=True)
        
        self.max_array = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        self.max_table = SparseTable(self.max_array, max, idempotent=True)
        
        self.sum_array = [5, 2, 8, 1, 9, 3, 7, 4, 6]
        self.sum_table = SparseTable(self.sum_array, lambda x, y: x + y, idempotent=False)
        
        # GCD function for testing
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
            
        self.gcd_array = [12, 6, 8, 24, 16, 20, 36, 48, 30]
        self.gcd_table = SparseTable(self.gcd_array, gcd, idempotent=True)
        
        # Empty table
        self.empty_table = SparseTable([], min, idempotent=True)
        
    def test_init(self):
        self.assertEqual(len(self.min_table), 9)
        self.assertEqual(self.min_table.n, 9)
        self.assertEqual(self.min_table.log_n, 4)  # log2(9) = 3.17, floor + 1 = 4
        self.assertEqual(len(self.min_table.table), 4)
        
        # Test empty table
        self.assertEqual(len(self.empty_table), 0)
        self.assertEqual(self.empty_table.log_n, 1)
        
    def test_min_query(self):
        # Test various ranges
        self.assertEqual(self.min_table.query(0, 8), 1)  # Entire array
        self.assertEqual(self.min_table.query(0, 2), 2)  # [5, 2, 8]
        self.assertEqual(self.min_table.query(3, 5), 1)  # [1, 9, 3]
        self.assertEqual(self.min_table.query(6, 8), 4)  # [7, 4, 6]
        
        # Single element queries
        for i in range(9):
            self.assertEqual(self.min_table.query(i, i), self.min_array[i])
            
        # Test idempotent specific method
        self.assertEqual(self.min_table.query_idempotent(2, 7), 1)
        
        # Test with invalid ranges
        with self.assertRaises(IndexError):
            self.min_table.query(-1, 5)
        with self.assertRaises(IndexError):
            self.min_table.query(3, 10)
        with self.assertRaises(IndexError):
            self.min_table.query(5, 2)
            
        # Test empty table
        with self.assertRaises(ValueError):
            self.empty_table.query(0, 0)
            
    def test_max_query(self):
        # Test various ranges
        self.assertEqual(self.max_table.query(0, 8), 9)  # Entire array
        self.assertEqual(self.max_table.query(0, 2), 8)  # [5, 2, 8]
        self.assertEqual(self.max_table.query(3, 5), 9)  # [1, 9, 3]
        self.assertEqual(self.max_table.query(6, 8), 7)  # [7, 4, 6]
        
        # Single element queries
        for i in range(9):
            self.assertEqual(self.max_table.query(i, i), self.max_array[i])
            
    def test_sum_query(self):
        # Test various ranges
        self.assertEqual(self.sum_table.query(0, 8), 45)  # Entire array
        self.assertEqual(self.sum_table.query(0, 2), 15)  # [5, 2, 8]
        self.assertEqual(self.sum_table.query(3, 5), 13)  # [1, 9, 3]
        self.assertEqual(self.sum_table.query(6, 8), 17)  # [7, 4, 6]
        
        # Single element queries
        for i in range(9):
            self.assertEqual(self.sum_table.query(i, i), self.sum_array[i])
            
        # Test non-idempotent specific method
        self.assertEqual(self.sum_table.query_non_idempotent(2, 7), 32)
            
    def test_gcd_query(self):
        # Test various ranges
        self.assertEqual(self.gcd_table.query(0, 8), 2)   # GCD of entire array
        self.assertEqual(self.gcd_table.query(0, 2), 2)   # GCD of [12, 6, 8]
        self.assertEqual(self.gcd_table.query(3, 5), 4)   # GCD of [24, 16, 20]
        self.assertEqual(self.gcd_table.query(6, 8), 6)   # GCD of [36, 48, 30]
        
        # Test specific intervals
        self.assertEqual(self.gcd_table.query(0, 1), 6)   # GCD of [12, 6]
        self.assertEqual(self.gcd_table.query(2, 3), 8)   # GCD of [8, 24]
        
    def test_idempotent_vs_non_idempotent(self):
        # Create a custom operation for testing
        def op(x, y):
            return x + y
            
        # Array for testing
        array = [1, 2, 3, 4, 5]
        
        # Create two tables with the same operation but different idempotent flags
        idempotent_table = SparseTable(array, op, idempotent=True)
        non_idempotent_table = SparseTable(array, op, idempotent=False)
        
        # For idempotent operations, the results will be incorrect for sum
        # For non-idempotent operations, they should be correct
        
        # Test a range query
        self.assertNotEqual(idempotent_table.query(0, 4), 15)  # Incorrect for sum: 1+5=6
        self.assertEqual(non_idempotent_table.query(0, 4), 15)  # Correct: 1+2+3+4+5=15
        
        # But both should work correctly if we explicitly call the right method
        self.assertEqual(idempotent_table.query_non_idempotent(0, 4), 15)  # Correct
        self.assertEqual(non_idempotent_table.query_non_idempotent(0, 4), 15)  # Correct
        
    def test_large_array(self):
        # Test with a larger array
        large_array = list(range(1000))
        min_table = SparseTable(large_array, min)
        max_table = SparseTable(large_array, max)
        sum_table = SparseTable(large_array, lambda x, y: x + y, idempotent=False)
        
        # Test min
        self.assertEqual(min_table.query(50, 150), 50)
        self.assertEqual(min_table.query(500, 999), 500)
        
        # Test max
        self.assertEqual(max_table.query(50, 150), 150)
        self.assertEqual(max_table.query(500, 999), 999)
        
        # Test sum
        self.assertEqual(sum_table.query(50, 150), sum(large_array[50:151]))
        self.assertEqual(sum_table.query(500, 999), sum(large_array[500:1000]))

if __name__ == '__main__':
    unittest.main()
