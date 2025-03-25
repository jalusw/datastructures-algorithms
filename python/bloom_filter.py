import unittest
import math
import mmh3  # MurmurHash3 for efficient hashing
from typing import List, Callable, Any, Optional, Set, Union

class BloomFilter:
    """
    BloomFilter is a space-efficient probabilistic data structure used to test whether an element is a member of a set.
    
    False positive matches are possible, but false negatives are not. Elements can be added to the set,
    but not removed. The more elements that are added, the higher the probability of false positives.
    
    Methods:
        - add(item) add an item to the filter
        - contains(item) check if an item might be in the filter
        - clear() remove all items from the filter
    """
    def __init__(self, capacity: int = 1000, error_rate: float = 0.01, hash_functions: Optional[List[Callable]] = None):
        """
        Initialize a Bloom filter.
        
        Args:
            capacity: Expected number of elements to be inserted
            error_rate: Desired false positive rate
            hash_functions: List of hash functions to use (if None, uses optimal number of MurmurHash3 functions)
        
        Raises:
            ValueError: If capacity is not positive or error_rate is not between 0 and 1
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
            
        if error_rate <= 0 or error_rate >= 1:
            raise ValueError("Error rate must be between 0 and 1")
            
        # Calculate optimal filter size based on capacity and error rate
        self.size = self._calculate_size(capacity, error_rate)
        
        # Calculate optimal number of hash functions
        self.num_hashes = self._calculate_hash_count(self.size, capacity)
        
        # Initialize bit array
        self.bit_array = [False] * self.size
        
        # Set hash functions
        self.hash_functions = hash_functions or self._create_hash_functions(self.num_hashes)
        
        # Store capacity and error rate for reference
        self.capacity = capacity
        self.error_rate = error_rate
        
        # Track inserted items count (for information purposes only)
        self.count = 0
        
    def __str__(self) -> str:
        """
        Return the string representation of the Bloom filter.
        """
        return f"BloomFilter(size={self.size}, hashes={self.num_hashes}, items={self.count})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the Bloom filter.
        """
        return self.__str__()
    
    def __len__(self) -> int:
        """
        Return the count of items added to the Bloom filter.
        Note: This is not the exact count as Bloom filters can't track exact membership.
        """
        return self.count
    
    def __contains__(self, item: Any) -> bool:
        """
        Check if the item might be in the Bloom filter.
        
        Args:
            item: The item to check
            
        Returns:
            True if the item might be in the filter, False if it definitely is not
        """
        return self.contains(item)
    
    def _calculate_size(self, capacity: int, error_rate: float) -> int:
        """
        Calculate the optimal size of the bit array.
        
        Args:
            capacity: Expected number of elements
            error_rate: Desired false positive rate
            
        Returns:
            The optimal size of the bit array
        """
        # m = -(n * ln(p)) / (ln(2)^2)
        # where m is size, n is capacity, p is error_rate
        size = -1 * capacity * math.log(error_rate) / (math.log(2) ** 2)
        return max(1, int(size))
    
    def _calculate_hash_count(self, size: int, capacity: int) -> int:
        """
        Calculate the optimal number of hash functions.
        
        Args:
            size: Size of the bit array
            capacity: Expected number of elements
            
        Returns:
            The optimal number of hash functions
        """
        # k = (m/n) * ln(2)
        # where k is number of hashes, m is size, n is capacity
        hash_count = (size / capacity) * math.log(2)
        return max(1, int(hash_count))
    
    def _create_hash_functions(self, num_hashes: int) -> List[Callable]:
        """
        Create the specified number of hash functions.
        Uses MurmurHash3 with different seeds.
        
        Args:
            num_hashes: Number of hash functions to create
            
        Returns:
            List of hash functions
        """
        return [lambda x, seed=i: mmh3.hash(repr(x), seed) % self.size for i in range(num_hashes)]
        
    def add(self, item: Any) -> None:
        """
        Add an item to the Bloom filter.
        
        Args:
            item: The item to add
        """
        for hash_func in self.hash_functions:
            index = hash_func(item)
            self.bit_array[index] = True
            
        self.count += 1
        
    def contains(self, item: Any) -> bool:
        """
        Check if the item might be in the Bloom filter.
        
        Args:
            item: The item to check
            
        Returns:
            True if the item might be in the filter, False if it definitely is not
        """
        for hash_func in self.hash_functions:
            index = hash_func(item)
            if not self.bit_array[index]:
                return False
                
        return True
        
    def clear(self) -> None:
        """
        Remove all items from the Bloom filter.
        """
        self.bit_array = [False] * self.size
        self.count = 0
    
    def current_false_positive_rate(self) -> float:
        """
        Calculate the current estimated false positive rate.
        
        Returns:
            The estimated false positive probability
        """
        # p = (1 - e^(-k*n/m))^k
        # where k is number of hashes, n is number of items, m is bit array size
        if self.count == 0:
            return 0.0
            
        return (1 - math.exp(-self.num_hashes * self.count / self.size)) ** self.num_hashes
    
    def union(self, other: 'BloomFilter') -> 'BloomFilter':
        """
        Create a new Bloom filter that is the union of this filter and another.
        
        Args:
            other: Another Bloom filter
            
        Returns:
            A new Bloom filter containing items from both filters
            
        Raises:
            ValueError: If the filters have different sizes or hash functions
        """
        if self.size != other.size or self.num_hashes != other.num_hashes:
            raise ValueError("Bloom filters must have the same size and number of hash functions")
            
        result = BloomFilter(self.capacity, self.error_rate, self.hash_functions)
        result.bit_array = [a or b for a, b in zip(self.bit_array, other.bit_array)]
        result.count = self.count + other.count  # Approximation
        
        return result


class TestBloomFilter(unittest.TestCase):
    def setUp(self):
        self.filter = BloomFilter(capacity=1000, error_rate=0.01)
        self.small_filter = BloomFilter(capacity=100, error_rate=0.1)
        
    def test_init(self):
        self.assertEqual(len(self.filter), 0)
        self.assertGreater(self.filter.size, 0)
        self.assertGreater(self.filter.num_hashes, 0)
        
        # Test invalid parameters
        with self.assertRaises(ValueError):
            BloomFilter(capacity=0)
            
        with self.assertRaises(ValueError):
            BloomFilter(error_rate=0)
            
        with self.assertRaises(ValueError):
            BloomFilter(error_rate=1.5)
            
    def test_add_contains(self):
        # Test that items added to the filter are contained
        items = ["apple", "banana", "cherry", "date", "elderberry"]
        
        for item in items:
            self.filter.add(item)
            
        for item in items:
            self.assertTrue(self.filter.contains(item))
            self.assertTrue(item in self.filter)  # Test __contains__
            
        # Test length after adding items
        self.assertEqual(len(self.filter), 5)
            
    def test_negative_containment(self):
        # Test that items not added are likely not contained 
        # (but false positives are possible)
        items = ["apple", "banana", "cherry", "date", "elderberry"]
        not_added = ["fig", "grape", "honeydew", "imbe", "jackfruit"]
        
        # Add only some items
        for item in items:
            self.filter.add(item)
            
        # Items not added should generally not be contained
        # Note: This is probabilistic, but with our low error rate, 
        # it's very unlikely to get false positives in this small test
        false_positives = 0
        for item in not_added:
            if item in self.filter:
                false_positives += 1
                
        # With a 0.01 error rate, it's unlikely to get even one false positive
        # from just 5 items, but it's still possible
        self.assertLessEqual(false_positives, 1)
        
    def test_clear(self):
        items = ["apple", "banana", "cherry"]
        
        for item in items:
            self.filter.add(item)
            
        self.assertEqual(len(self.filter), 3)
        
        self.filter.clear()
        self.assertEqual(len(self.filter), 0)
        
        for item in items:
            self.assertFalse(item in self.filter)
            
    def test_false_positive_rate(self):
        # Create a filter with very high error rate for testing
        high_error_filter = BloomFilter(capacity=100, error_rate=0.5)
        
        # Initially, with no items, false positive rate should be 0
        self.assertEqual(high_error_filter.current_false_positive_rate(), 0.0)
        
        # Add some items
        for i in range(50):
            high_error_filter.add(f"item{i}")
            
        # Check that the false positive rate increases
        self.assertGreater(high_error_filter.current_false_positive_rate(), 0.0)
        
        # Check that the error rate is close to expected
        # Note: This is just a rough approximation, not exact
        self.assertLess(abs(high_error_filter.current_false_positive_rate() - 0.5), 0.3)
        
    def test_union(self):
        filter1 = BloomFilter(capacity=1000, error_rate=0.01)
        filter2 = BloomFilter(capacity=1000, error_rate=0.01)
        
        # Add different items to each filter
        for i in range(100):
            filter1.add(f"item1_{i}")
            
        for i in range(100):
            filter2.add(f"item2_{i}")
            
        # Create union
        union_filter = filter1.union(filter2)
        
        # Check that union contains items from both filters
        for i in range(100):
            self.assertTrue(f"item1_{i}" in union_filter)
            self.assertTrue(f"item2_{i}" in union_filter)
            
        # Check that the original filters are unchanged
        self.assertEqual(len(filter1), 100)
        self.assertEqual(len(filter2), 100)
        
        # Test union with incompatible filters
        different_filter = BloomFilter(capacity=500, error_rate=0.05)
        with self.assertRaises(ValueError):
            filter1.union(different_filter)
            
    def test_different_capacities(self):
        # Test that filters with different capacities have different sizes
        small_filter = BloomFilter(capacity=100, error_rate=0.01)
        large_filter = BloomFilter(capacity=10000, error_rate=0.01)
        
        self.assertLess(small_filter.size, large_filter.size)
        
    def test_different_error_rates(self):
        # Test that filters with different error rates have different sizes
        precise_filter = BloomFilter(capacity=1000, error_rate=0.001)
        imprecise_filter = BloomFilter(capacity=1000, error_rate=0.1)
        
        self.assertGreater(precise_filter.size, imprecise_filter.size)
        
    def test_custom_hash_functions(self):
        # Test using custom hash functions
        def hash1(x):
            return hash(str(x) + "salt1") % 1000
            
        def hash2(x):
            return hash(str(x) + "salt2") % 1000
            
        custom_filter = BloomFilter(capacity=1000, error_rate=0.01, hash_functions=[hash1, hash2])
        
        self.assertEqual(len(custom_filter.hash_functions), 2)
        
        # Test that the filter works with custom hash functions
        items = ["apple", "banana", "cherry"]
        
        for item in items:
            custom_filter.add(item)
            
        for item in items:
            self.assertTrue(item in custom_filter)

if __name__ == '__main__':
    unittest.main()
