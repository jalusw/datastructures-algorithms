from typing import TypeVar, Optional, List, Any
import random
import math

T = TypeVar('T')

class SkipListNode:
    """Node in a skip list."""
    def __init__(self, key: T, value: Any, level: int):
        self.key = key
        self.value = value
        self.forward: List[Optional['SkipListNode']] = [None] * level
        self.level = level

class SkipList:
    """
    A probabilistic data structure that provides O(log n) average case complexity
    for search, insert, and delete operations.
    
    The skip list is a linked list with multiple levels, where each level is a
    subset of the level below it. The top level contains the fewest elements,
    while the bottom level contains all elements.
    
    Properties:
        - O(log n) average case complexity for operations
        - O(n) worst case complexity
        - O(n) space complexity
        - Probabilistic balancing
        - Supports duplicate keys
    """
    
    def __init__(self, max_level: int = 16, probability: float = 0.5):
        """
        Initialize a skip list.
        
        Args:
            max_level: Maximum number of levels in the skip list
            probability: Probability of promoting a node to the next level
        """
        self.max_level = max_level
        self.probability = probability
        self.head = SkipListNode(float('-inf'), None, max_level)
        self.tail = SkipListNode(float('inf'), None, max_level)
        self.size = 0
        
        # Connect all levels of head to tail
        for i in range(max_level):
            self.head.forward[i] = self.tail
    
    def _random_level(self) -> int:
        """
        Generate a random level for a new node.
        
        Returns:
            A random level between 1 and max_level
        """
        level = 1
        while random.random() < self.probability and level < self.max_level:
            level += 1
        return level
    
    def insert(self, key: T, value: Any) -> None:
        """
        Insert a key-value pair into the skip list.
        
        Args:
            key: The key to insert
            value: The value associated with the key
        """
        # Keep track of nodes at each level that need to be updated
        update = [self.head] * self.max_level
        current = self.head
        
        # Find the position to insert the new node
        for i in range(self.max_level - 1, -1, -1):
            while current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        # Generate random level for the new node
        new_level = self._random_level()
        new_node = SkipListNode(key, value, new_level)
        
        # Update the forward pointers
        for i in range(new_level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
        
        self.size += 1
    
    def search(self, key: T) -> Optional[Any]:
        """
        Search for a key in the skip list.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key if found, None otherwise
        """
        current = self.head
        
        # Start from the highest level and move down
        for i in range(self.max_level - 1, -1, -1):
            while current.forward[i].key < key:
                current = current.forward[i]
            if current.forward[i].key == key:
                return current.forward[i].value
        
        return None
    
    def delete(self, key: T) -> bool:
        """
        Delete a key from the skip list.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was found and deleted, False otherwise
        """
        # Keep track of nodes at each level that need to be updated
        update = [self.head] * self.max_level
        current = self.head
        
        # Find the node to delete
        for i in range(self.max_level - 1, -1, -1):
            while current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        
        # If the key is found, update the forward pointers
        if current.forward[0].key == key:
            node_to_delete = current.forward[0]
            for i in range(node_to_delete.level):
                update[i].forward[i] = node_to_delete.forward[i]
            self.size -= 1
            return True
        
        return False
    
    def get_min(self) -> Optional[Any]:
        """
        Get the minimum key in the skip list.
        
        Returns:
            The value associated with the minimum key if the list is not empty,
            None otherwise
        """
        if self.size == 0:
            return None
        return self.head.forward[0].value
    
    def get_max(self) -> Optional[Any]:
        """
        Get the maximum key in the skip list.
        
        Returns:
            The value associated with the maximum key if the list is not empty,
            None otherwise
        """
        if self.size == 0:
            return None
        current = self.head
        while current.forward[0] != self.tail:
            current = current.forward[0]
        return current.value
    
    def clear(self) -> None:
        """Clear all elements from the skip list."""
        self.head = SkipListNode(float('-inf'), None, self.max_level)
        self.tail = SkipListNode(float('inf'), None, self.max_level)
        for i in range(self.max_level):
            self.head.forward[i] = self.tail
        self.size = 0
    
    def __len__(self) -> int:
        """Return the number of elements in the skip list."""
        return self.size
    
    def __contains__(self, key: T) -> bool:
        """Check if a key exists in the skip list."""
        return self.search(key) is not None
    
    def __getitem__(self, key: T) -> Any:
        """Get the value associated with a key."""
        value = self.search(key)
        if value is None:
            raise KeyError(f"Key {key} not found")
        return value
    
    def __setitem__(self, key: T, value: Any) -> None:
        """Set the value associated with a key."""
        self.insert(key, value)
    
    def __delitem__(self, key: T) -> None:
        """Delete a key from the skip list."""
        if not self.delete(key):
            raise KeyError(f"Key {key} not found") 