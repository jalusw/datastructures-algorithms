import unittest

class Stack:
    """
    Stack is a LIFO (last-in, first-out) data structure.
    
    Methods:
        - push(value) add value to the top of the stack
        - pop() remove and return the top element
        - peek() return the top element without removing it
    """
    def __init__(self):
        """
        Initialize an empty stack.
        """
        self.items = []
        
    def __str__(self) -> str:
        """
        Return the string representation of the stack.
        """
        return f"{self.items}"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the stack.
        """
        return f"Stack({self.items})"
        
    def __len__(self) -> int:
        """
        Return the length of the stack.
        """
        return len(self.items)
        
    def __contains__(self, value) -> bool:
        """
        Check if the value is in the stack.
        
        Args:
            value: the value to check
        """
        return value in self.items
        
    def push(self, value) -> None:
        """
        Add value to the top of the stack.
        
        Args:
            value: the value to add
        """
        self.items.append(value)
        
    def pop(self):
        """
        Remove and return the top element.
        
        Returns:
            The top element
            
        Raises:
            IndexError: if the stack is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot pop from an empty stack")
        return self.items.pop()
        
    def peek(self):
        """
        Return the top element without removing it.
        
        Returns:
            The top element
            
        Raises:
            IndexError: if the stack is empty
        """
        if len(self.items) == 0:
            raise IndexError("Cannot peek at an empty stack")
        return self.items[-1]
        
    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        
        Returns:
            True if the stack is empty, False otherwise
        """
        return len(self.items) == 0


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()
        
    def test_init(self):
        self.assertEqual(self.stack.items, [])
        self.assertEqual(len(self.stack), 0)
        self.assertTrue(self.stack.is_empty())
        
    def test_push(self):
        self.stack.push(1)
        self.assertEqual(self.stack.items, [1])
        self.assertEqual(len(self.stack), 1)
        self.assertFalse(self.stack.is_empty())
        
        self.stack.push(2)
        self.assertEqual(self.stack.items, [1, 2])
        self.assertEqual(len(self.stack), 2)
        
    def test_pop(self):
        with self.assertRaises(IndexError):
            self.stack.pop()
            
        self.stack.push(1)
        self.stack.push(2)
        
        value = self.stack.pop()
        self.assertEqual(value, 2)
        self.assertEqual(self.stack.items, [1])
        self.assertEqual(len(self.stack), 1)
        
    def test_peek(self):
        with self.assertRaises(IndexError):
            self.stack.peek()
            
        self.stack.push(1)
        self.stack.push(2)
        
        value = self.stack.peek()
        self.assertEqual(value, 2)
        self.assertEqual(self.stack.items, [1, 2])  # Ensure stack is unchanged
        self.assertEqual(len(self.stack), 2)
        
    def test_contains(self):
        self.stack.push(1)
        self.stack.push(3)
        self.assertFalse(2 in self.stack)
        self.assertTrue(1 in self.stack)
        
    def test_lifo_order(self):
        for i in range(5):
            self.stack.push(i)
            
        for i in range(4, -1, -1):
            self.assertEqual(self.stack.pop(), i)
            
        self.assertTrue(self.stack.is_empty())

if __name__ == '__main__':
    unittest.main()
