import unittest

class Node:
    """
    A node in a singly linked list.
    
    Attributes:
        value: The value stored in the node
        next: Reference to the next node
    """
    def __init__(self, value):
        self.value = value
        self.next = None

class SinglyLinkedList:
    """
    SinglyLinkedList is a data structure where each element points to the next.
    
    Methods:
        - append(value) append value to the end of the list
        - prepend(value) add value to the beginning of the list
        - pop() remove and return the last element
        - remove(index) remove element at specified index
        - lookup(index) return value at specified index
        - traverse() return all values in the list
    """
    def __init__(self):
        """
        Initialize an empty linked list.
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
        return f"SinglyLinkedList({self.__str__()})"
    
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
        
        current = self.head
        for i in range(index):
            current = current.next
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
            
        if self.head == self.tail:
            value = self.head.value
            self.head = None
            self.tail = None
            self.length = 0
            return value
            
        current = self.head
        while current.next != self.tail:
            current = current.next
            
        value = self.tail.value
        current.next = None
        self.tail = current
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
            self.head = self.head.next
            if not self.head:
                self.tail = None
            self.length -= 1
            return
            
        current = self.head
        for i in range(index - 1):
            current = current.next
            
        # If removing the last element, update tail
        if current.next == self.tail:
            self.tail = current
            
        current.next = current.next.next
        self.length -= 1

    def traverse(self):
        """
        Return all values in the list.
        
        Returns:
            A list containing all values
        """
        values = []
        current = self.head
        while current:
            values.append(current.value)
            current = current.next
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


class TestSinglyLinkedList(unittest.TestCase):
    def setUp(self):
        self.list = SinglyLinkedList()

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

    def test_prepend(self):
        self.list.prepend(1)
        self.assertEqual(self.list.head.value, 1)
        self.assertEqual(len(self.list), 1)
        
        self.list.prepend(2)
        self.assertEqual(self.list.head.value, 2)
        self.assertEqual(self.list.tail.value, 1)
        self.assertEqual(len(self.list), 2)

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

    def test_remove(self):
        with self.assertRaises(IndexError):
            self.list.remove(0)
            
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        
        self.list.remove(1)
        self.assertEqual(len(self.list), 2)
        self.assertEqual(self.list.head.value, 1)
        self.assertEqual(self.list.tail.value, 3)
        
        with self.assertRaises(IndexError):
            self.list.remove(5)

    def test_traverse(self):
        self.assertEqual(self.list.traverse(), [])
        
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        
        self.assertEqual(self.list.traverse(), [1, 2, 3])

    def test_lookup(self):
        with self.assertRaises(IndexError):
            self.list.lookup(0)
            
        self.list.append(10)
        self.list.append(20)
        
        self.assertEqual(self.list.lookup(0), 10)
        self.assertEqual(self.list.lookup(1), 20)
        
        with self.assertRaises(IndexError):
            self.list.lookup(2)
            
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

if __name__ == '__main__':
    unittest.main()
