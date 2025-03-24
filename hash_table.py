import unittest
from typing import Any, List, Optional, Tuple
from collections import deque

class HashNode:
    """
    A node in a Hash Table.
    
    Attributes:
        key: The key stored in this node
        value: The value associated with the key
        is_deleted: Whether this node has been deleted
    """
    def __init__(self, key: Any, value: Any):
        """
        Initialize a Hash Table node.
        
        Args:
            key: The key to store
            value: The value to associate with the key
        """
        self.key = key
        self.value = value
        self.is_deleted = False

class HashTable:
    """
    A Hash Table is a data structure that implements an associative array abstract data type,
    a structure that can map keys to values. It uses a hash function to compute an index into
    an array of buckets or slots, from which the desired value can be found.
    
    This implementation uses open addressing with linear probing for collision resolution.
    
    Methods:
        - insert(key, value) add a key-value pair
        - delete(key) remove a key-value pair
        - get(key) get the value associated with a key
        - contains(key) check if a key exists
        - clear() remove all key-value pairs
        - size() get the number of key-value pairs
    """
    def __init__(self, initial_size: int = 16, load_factor: float = 0.75):
        """
        Initialize an empty Hash Table.
        
        Args:
            initial_size: The initial size of the hash table (default: 16)
            load_factor: The maximum load factor before resizing (default: 0.75)
        """
        self.size = 0
        self.capacity = initial_size
        self.load_factor = load_factor
        self.table: List[Optional[HashNode]] = [None] * initial_size
        
    def __str__(self) -> str:
        """
        Return the string representation of the hash table.
        """
        return f"HashTable(size={self.size}, capacity={self.capacity})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the hash table.
        """
        return self.__str__()
        
    def _hash(self, key: Any) -> int:
        """
        Compute the hash value for a key.
        
        Args:
            key: The key to hash
            
        Returns:
            The hash value
        """
        if isinstance(key, int):
            return key % self.capacity
        return hash(key) % self.capacity
        
    def _probe(self, key: Any, start_index: int) -> int:
        """
        Find the next available slot using linear probing.
        
        Args:
            key: The key to find a slot for
            start_index: The initial index to start probing from
            
        Returns:
            The index of the next available slot
        """
        index = start_index
        first_deleted = -1
        
        while True:
            if self.table[index] is None:
                return first_deleted if first_deleted != -1 else index
            if self.table[index].is_deleted and first_deleted == -1:
                first_deleted = index
            if not self.table[index].is_deleted and self.table[index].key == key:
                return index
            index = (index + 1) % self.capacity
            if index == start_index:
                return -1  # Table is full
                
    def _resize(self) -> None:
        """
        Resize the hash table when the load factor is exceeded.
        """
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        
        for node in old_table:
            if node is not None and not node.is_deleted:
                self.insert(node.key, node.value)
                
    def insert(self, key: Any, value: Any) -> None:
        """
        Insert a key-value pair into the hash table.
        
        Args:
            key: The key to insert
            value: The value to associate with the key
        """
        if self.size / self.capacity >= self.load_factor:
            self._resize()
            
        index = self._probe(key, self._hash(key))
        if index == -1:
            raise RuntimeError("Hash table is full")
            
        if self.table[index] is None or self.table[index].is_deleted:
            self.table[index] = HashNode(key, value)
            self.size += 1
        else:
            self.table[index].value = value
            
    def get(self, key: Any) -> Optional[Any]:
        """
        Get the value associated with a key.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or None if not found
        """
        index = self._probe(key, self._hash(key))
        if index == -1 or self.table[index] is None or self.table[index].is_deleted:
            return None
        return self.table[index].value
        
    def delete(self, key: Any) -> bool:
        """
        Delete a key-value pair from the hash table.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was deleted, False if it wasn't found
        """
        index = self._probe(key, self._hash(key))
        if index == -1 or self.table[index] is None or self.table[index].is_deleted:
            return False
            
        self.table[index].is_deleted = True
        self.size -= 1
        return True
        
    def contains(self, key: Any) -> bool:
        """
        Check if a key exists in the hash table.
        
        Args:
            key: The key to check for
            
        Returns:
            True if the key exists, False otherwise
        """
        return self.get(key) is not None
        
    def clear(self) -> None:
        """
        Remove all key-value pairs from the hash table.
        """
        self.table = [None] * self.capacity
        self.size = 0
        
    def keys(self) -> List[Any]:
        """
        Get all keys in the hash table.
        
        Returns:
            List of all keys
        """
        return [node.key for node in self.table if node is not None and not node.is_deleted]
        
    def values(self) -> List[Any]:
        """
        Get all values in the hash table.
        
        Returns:
            List of all values
        """
        return [node.value for node in self.table if node is not None and not node.is_deleted]
        
    def items(self) -> List[Tuple[Any, Any]]:
        """
        Get all key-value pairs in the hash table.
        
        Returns:
            List of (key, value) tuples
        """
        return [(node.key, node.value) for node in self.table if node is not None and not node.is_deleted]


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.table = HashTable()
        
    def test_init(self):
        self.assertEqual(self.table.size, 0)
        self.assertEqual(self.table.capacity, 16)
        self.assertEqual(self.table.load_factor, 0.75)
        
    def test_insert(self):
        self.table.insert("key1", "value1")
        self.assertEqual(self.table.size, 1)
        self.assertEqual(self.table.get("key1"), "value1")
        
        # Test overwriting
        self.table.insert("key1", "new_value")
        self.assertEqual(self.table.size, 1)
        self.assertEqual(self.table.get("key1"), "new_value")
        
    def test_get(self):
        self.table.insert("key1", "value1")
        self.assertEqual(self.table.get("key1"), "value1")
        self.assertIsNone(self.table.get("nonexistent"))
        
    def test_delete(self):
        self.table.insert("key1", "value1")
        self.assertTrue(self.table.delete("key1"))
        self.assertEqual(self.table.size, 0)
        self.assertIsNone(self.table.get("key1"))
        self.assertFalse(self.table.delete("nonexistent"))
        
    def test_contains(self):
        self.table.insert("key1", "value1")
        self.assertTrue(self.table.contains("key1"))
        self.assertFalse(self.table.contains("nonexistent"))
        
    def test_clear(self):
        self.table.insert("key1", "value1")
        self.table.insert("key2", "value2")
        self.table.clear()
        self.assertEqual(self.table.size, 0)
        self.assertIsNone(self.table.get("key1"))
        self.assertIsNone(self.table.get("key2"))
        
    def test_keys_values_items(self):
        self.table.insert("key1", "value1")
        self.table.insert("key2", "value2")
        
        self.assertEqual(set(self.table.keys()), {"key1", "key2"})
        self.assertEqual(set(self.table.values()), {"value1", "value2"})
        self.assertEqual(set(self.table.items()), {("key1", "value1"), ("key2", "value2")})
        
    def test_resize(self):
        # Fill the table beyond load factor
        for i in range(13):  # 13/16 > 0.75
            self.table.insert(f"key{i}", f"value{i}")
            
        self.assertEqual(self.table.capacity, 32)  # Should have doubled
        self.assertEqual(self.table.size, 13)
        
        # Verify all values are still accessible
        for i in range(13):
            self.assertEqual(self.table.get(f"key{i}"), f"value{i}")
            
    def test_collision_handling(self):
        # Force collisions by using same hash
        self.table.insert(0, "value0")
        self.table.insert(16, "value16")  # Will collide with 0
        self.table.insert(32, "value32")  # Will collide with 0 and 16
        
        self.assertEqual(self.table.get(0), "value0")
        self.assertEqual(self.table.get(16), "value16")
        self.assertEqual(self.table.get(32), "value32")
        
    def test_deleted_nodes(self):
        self.table.insert("key1", "value1")
        self.table.insert("key2", "value2")
        self.table.delete("key1")
        
        # Should not find deleted key
        self.assertIsNone(self.table.get("key1"))
        
        # Should still find non-deleted key
        self.assertEqual(self.table.get("key2"), "value2")
        
        # Should be able to reuse deleted slot
        self.table.insert("key3", "value3")
        self.assertEqual(self.table.get("key3"), "value3")
        
    def test_different_types(self):
        # Test with different key types
        self.table.insert(1, "int")
        self.table.insert("string", "str")
        self.table.insert(1.5, "float")
        self.table.insert(True, "bool")
        self.table.insert(None, "none")
        
        self.assertEqual(self.table.get(1), "int")
        self.assertEqual(self.table.get("string"), "str")
        self.assertEqual(self.table.get(1.5), "float")
        self.assertEqual(self.table.get(True), "bool")
        self.assertEqual(self.table.get(None), "none")

 