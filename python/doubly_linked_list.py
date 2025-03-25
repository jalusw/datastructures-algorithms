import unittest

class Node:
    """
    A node in a doubly linked list.
    
    Attributes:
        value: The value stored in the node
        next: Reference to the next node
        prev: Reference to the previous node
    """
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class DoublyLinkedList:
    """
    DoublyLinkedList is a data structure where each element points to the next and previous elements.
    
    Methods:
        - append(value) append value to the end of the list
        - prepend(value) add value to the beginning of the list
        - pop() remove and return the last element
        - pop_first() remove and return the first element
        - remove(index) remove element at specified index
        - lookup(index) return value at specified index
        - traverse() return all values in the list
        - reverse_traverse() return all values in the list in reverse order
    """
    def __init__(self):
        """
        Initialize an empty doubly linked list.
        """
        self.head = None
        self.tail = None
        self.length = 0

    def __str__(self) -> str:
        """
        Return the string representation of the list.
        """
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return f"[{', '.join(values)}]"

    def __repr__(self) -> str:
        """
        Return the string representation of the list.
        """
        return f"DoublyLinkedList({self.__str__()})"
    
    def __len__(self) -> int:
        """
        Return the length of the list.
        """
        return self.length
    
    def __contains__(self, value) -> bool:
        """
        Check if the value is in the list.
        
        Args:
            value: the value to check
        """
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False
    
    def __getitem__(self, index):
        """
        Return the value at the specified index.
        
        Args:
            index: the index of the value to return
            
        Raises:
            IndexError: if the index is out of range
        """
        if index >= self.length or index < 0:
            raise IndexError("Index out of range")
        
        # Optimize lookup by approaching from the appropriate end
        if index < self.length // 2:
            # Approach from head
            current = self.head
            for i in range(index):
                current = current.next
        else:
            # Approach from tail
            current = self.tail
            for i in range(self.length - 1, index, -1):
                current = current.prev
                
        return current.value

    def append(self, value) -> None:
        """
        Append the value to the end of the list.
        
        Args:
            value: the value to append
        """
        new_node = Node(value)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            
        self.length += 1
    
    def prepend(self, value) -> None:
        """
        Add the value to the beginning of the list.
        
        Args:
            value: the value to prepend
        """
        new_node = Node(value)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            
        self.length += 1

    def pop(self):
        """
        Remove and return the last element.
        
        Returns:
            The value of the removed element
            
        Raises:
            IndexError: if the list is empty
        """
        if not self.head:
            raise IndexError("Cannot pop from an empty list")
            
        value = self.tail.value
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            
        self.length -= 1
        return value
    
    def pop_first(self):
        """
        Remove and return the first element.
        
        Returns:
            The value of the removed element
            
        Raises:
            IndexError: if the list is empty
        """
        if not self.head:
            raise IndexError("Cannot pop_first from an empty list")
            
        value = self.head.value
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
            
        self.length -= 1
        return value
    
    def remove(self, index) -> None:
        """
        Remove the element at the specified index.
        
        Args:
            index: the index of the element to remove
            
        Raises:
            IndexError: if the index is out of range
        """
        if index >= self.length or index < 0:
            raise IndexError("Index out of range")
            
        if index == 0:
            self.pop_first()
            return
            
        if index == self.length - 1:
            self.pop()
            return
        
        # Find the node to remove
        if index < self.length // 2:
            # Approach from head
            current = self.head
            for i in range(index):
                current = current.next
        else:
            # Approach from tail
            current = self.tail
            for i in range(self.length - 1, index, -1):
                current = current.prev
        
        # Update links to skip the current node
        current.prev.next = current.next
        current.next.prev = current.prev
        
        self.length -= 1

    def traverse(self):
        """
        Return all values in the list from head to tail.
        
        Returns:
            A list containing all values
        """
        values = []
        current = self.head
        while current:
            values.append(current.value)
            current = current.next
        return values
    
    def reverse_traverse(self):
        """
        Return all values in the list from tail to head.
        
        Returns:
            A list containing all values in reverse order
        """
        values = []
        current = self.tail
        while current:
            values.append(current.value)
            current = current.prev
        return values

    def lookup(self, index):
        """
        Return the value at the specified index.
        
        Args:
            index: the index of the value to return
            
        Raises:
            IndexError: if the index is out of range
        """
        return self.__getitem__(index)
    
    def insert(self, index, value) -> None:
        """
        Insert a value at the specified index.
        
        Args:
            index: the index at which to insert the value
            value: the value to insert
            
        Raises:
            IndexError: if the index is out of range
        """
        if index > self.length or index < 0:
            raise IndexError("Index out of range")
            
        if index == 0:
            self.prepend(value)
            return
            
        if index == self.length:
            self.append(value)
            return
        
        new_node = Node(value)
        
        # Find the node at the position where we want to insert
        if index < self.length // 2:
            # Approach from head
            current = self.head
            for i in range(index):
                current = current.next
        else:
            # Approach from tail
            current = self.tail
            for i in range(self.length - 1, index, -1):
                current = current.prev
        
        # Insert new_node before current
        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node
        
        self.length += 1
    
    def clear(self) -> None:
        """
        Remove all elements from the list.
        """
        self.head = None
        self.tail = None
        self.length = 0


class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.list = DoublyLinkedList()

    def test_init(self):
        self.assertIsNone(self.list.head)
        self.assertIsNone(self.list.tail)
        self.assertEqual(len(self.list), 0)

    def test_append(self):
        self.list.append(1)
        self.assertEqual(self.list.head.value, 1)
        self.assertEqual(self.list.tail.value, 1)
        self.assertEqual(len(self.list), 1)
        
        self.list.append(2)
        self.assertEqual(self.list.head.value, 1)
        self.assertEqual(self.list.tail.value, 2)
        self.assertEqual(len(self.list), 2)
        
        # Test prev links
        self.assertIsNone(self.list.head.prev)
        self.assertEqual(self.list.tail.prev, self.list.head)

    def test_prepend(self):
        self.list.prepend(1)
        self.assertEqual(self.list.head.value, 1)
        self.assertEqual(len(self.list), 1)
        
        self.list.prepend(2)
        self.assertEqual(self.list.head.value, 2)
        self.assertEqual(self.list.tail.value, 1)
        self.assertEqual(len(self.list), 2)
        
        # Test prev links
        self.assertIsNone(self.list.head.prev)
        self.assertEqual(self.list.tail.prev, self.list.head)

    def test_pop(self):
        with self.assertRaises(IndexError):
            self.list.pop()
            
        self.list.append(1)
        self.list.append(2)
        
        value = self.list.pop()
        self.assertEqual(value, 2)
        self.assertEqual(len(self.list), 1)
        self.assertEqual(self.list.head.value, 1)
        self.assertEqual(self.list.tail.value, 1)
        self.assertIsNone(self.list.tail.next)

    def test_pop_first(self):
        with self.assertRaises(IndexError):
            self.list.pop_first()
            
        self.list.append(1)
        self.list.append(2)
        
        value = self.list.pop_first()
        self.assertEqual(value, 1)
        self.assertEqual(len(self.list), 1)
        self.assertEqual(self.list.head.value, 2)
        self.assertEqual(self.list.tail.value, 2)
        self.assertIsNone(self.list.head.prev)

    def test_remove(self):
        with self.assertRaises(IndexError):
            self.list.remove(0)
            
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        
        self.list.remove(1)  # Remove middle element
        self.assertEqual(len(self.list), 2)
        self.assertEqual(self.list.head.value, 1)
        self.assertEqual(self.list.tail.value, 3)
        self.assertEqual(self.list.head.next, self.list.tail)
        self.assertEqual(self.list.tail.prev, self.list.head)
        
        with self.assertRaises(IndexError):
            self.list.remove(5)

    def test_traverse(self):
        self.assertEqual(self.list.traverse(), [])
        
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        
        self.assertEqual(self.list.traverse(), [1, 2, 3])

    def test_reverse_traverse(self):
        self.assertEqual(self.list.reverse_traverse(), [])
        
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        
        self.assertEqual(self.list.reverse_traverse(), [3, 2, 1])

    def test_lookup(self):
        with self.assertRaises(IndexError):
            self.list.lookup(0)
            
        self.list.append(10)
        self.list.append(20)
        self.list.append(30)
        
        self.assertEqual(self.list.lookup(0), 10)
        self.assertEqual(self.list.lookup(1), 20)
        self.assertEqual(self.list.lookup(2), 30)
        
        with self.assertRaises(IndexError):
            self.list.lookup(3)
    
    def test_efficient_lookup(self):
        # Test that lookup approaches from the correct end
        for i in range(10):
            self.list.append(i)
            
        # These should approach from the head
        self.assertEqual(self.list.lookup(0), 0)
        self.assertEqual(self.list.lookup(2), 2)
        
        # These should approach from the tail
        self.assertEqual(self.list.lookup(9), 9)
        self.assertEqual(self.list.lookup(7), 7)
            
    def test_contains(self):
        self.list.append(1)
        self.list.append(3)
        self.assertFalse(2 in self.list)
        self.assertTrue(1 in self.list)
        
    def test_getitem(self):
        self.list.append(10)
        self.list.append(20)
        
        self.assertEqual(self.list[0], 10)
        self.assertEqual(self.list[1], 20)
        
        with self.assertRaises(IndexError):
            self.list[2]

    def test_insert(self):
        # Insert at beginning (empty list)
        self.list.insert(0, 10)
        self.assertEqual(self.list.traverse(), [10])
        
        # Insert at end
        self.list.insert(1, 30)
        self.assertEqual(self.list.traverse(), [10, 30])
        
        # Insert in middle
        self.list.insert(1, 20)
        self.assertEqual(self.list.traverse(), [10, 20, 30])
        
        # Check links
        self.assertEqual(self.list.head.next.prev, self.list.head)
        self.assertEqual(self.list.tail.prev.next, self.list.tail)
        
        with self.assertRaises(IndexError):
            self.list.insert(5, 40)

    def test_clear(self):
        for i in range(5):
            self.list.append(i)
            
        self.assertEqual(len(self.list), 5)
        
        self.list.clear()
        self.assertEqual(len(self.list), 0)
        self.assertIsNone(self.list.head)
        self.assertIsNone(self.list.tail)

if __name__ == '__main__':
    unittest.main()
