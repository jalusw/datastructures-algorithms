import unittest

class MonotonicStack:
    """
    MonotonicStack is a data structure that maintains elements in monotonic order.
    
    Methods:
        - push(value) add value to the stack while maintaining monotonicity
        - pop() remove and return the top element
        - peek() return the top element without removing it
        - get_min() return the minimum value in the stack (for non-decreasing mode)
        - get_max() return the maximum value in the stack (for non-increasing mode)
    """
    
    INCREASING = "increasing"  # Min at bottom (for get_min())
    DECREASING = "decreasing"  # Max at bottom (for get_max())
    
    def __init__(self, mode=DECREASING):
        """
        Initialize an empty monotonic stack.
        
        Args:
            mode: "increasing" for a non-decreasing stack (supports get_min), 
                 "decreasing" for a non-increasing stack (supports get_max)
        
        Raises:
            ValueError: if mode is not "increasing" or "decreasing"
        """
        if mode not in [self.INCREASING, self.DECREASING]:
            raise ValueError("Mode must be 'increasing' or 'decreasing'")
            
        self.mode = mode
        self.items = []  # Main stack for elements
        self.monotonic = []  # Monotonic stack for min/max tracking
        
    def __str__(self) -> str:
        """
        Return the string representation of the stack.
        """
        return f"MonotonicStack({self.items}, mode={self.mode})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the stack.
        """
        return self.__str__()
        
    def __len__(self) -> int:
        """
        Return the number of elements in the stack.
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
        Add a value to the stack while maintaining monotonicity.
        
        Args:
            value: the value to add
        """
        # Add to the main stack
        self.items.append(value)
        
        # Update monotonic stack
        if self.mode == self.INCREASING:
            # For min stack (increasing): append if empty or value ≥ current min
            if not self.monotonic or value >= self.monotonic[-1]:
                self.monotonic.append(value)
            else:
                # For values less than the current min, record the new min
                self.monotonic.append(self.monotonic[-1])  # Keep the previous value
        else:
            # For max stack (decreasing): append if empty or value ≤ current max
            if not self.monotonic or value <= self.monotonic[-1]:
                self.monotonic.append(value)
            else:
                # For values greater than the current max, record the new max
                self.monotonic.append(self.monotonic[-1])  # Keep the previous value
                
    def pop(self):
        """
        Remove and return the top element.
        
        Returns:
            The top element
            
        Raises:
            IndexError: if the stack is empty
        """
        if not self.items:
            raise IndexError("Cannot pop from an empty stack")
            
        # Pop from monotonic stack too
        self.monotonic.pop()
            
        return self.items.pop()
        
    def peek(self):
        """
        Return the top element without removing it.
        
        Returns:
            The top element
            
        Raises:
            IndexError: if the stack is empty
        """
        if not self.items:
            raise IndexError("Cannot peek at an empty stack")
        return self.items[-1]
    
    def get_min(self):
        """
        Return the minimum value in the stack.
        This method is intended for use with mode="increasing".
        
        Returns:
            The minimum value
            
        Raises:
            IndexError: if the stack is empty
            RuntimeError: if the stack is not in "increasing" mode
        """
        if self.mode != self.INCREASING:
            raise RuntimeError("get_min() is only available for 'increasing' mode")
            
        if not self.monotonic:
            raise IndexError("Cannot get minimum from an empty stack")
            
        return self.monotonic[-1]
    
    def get_max(self):
        """
        Return the maximum value in the stack.
        This method is intended for use with mode="decreasing".
        
        Returns:
            The maximum value
            
        Raises:
            IndexError: if the stack is empty
            RuntimeError: if the stack is not in "decreasing" mode
        """
        if self.mode != self.DECREASING:
            raise RuntimeError("get_max() is only available for 'decreasing' mode")
            
        if not self.monotonic:
            raise IndexError("Cannot get maximum from an empty stack")
            
        return self.monotonic[-1]
    
    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        
        Returns:
            True if the stack is empty, False otherwise
        """
        return len(self.items) == 0
    
    def clear(self) -> None:
        """
        Remove all elements from the stack.
        """
        self.items.clear()
        self.monotonic.clear()


class TestMonotonicStack(unittest.TestCase):
    def setUp(self):
        self.min_stack = MonotonicStack(mode=MonotonicStack.INCREASING)
        self.max_stack = MonotonicStack(mode=MonotonicStack.DECREASING)
        
    def test_init(self):
        self.assertEqual(len(self.min_stack), 0)
        self.assertEqual(len(self.max_stack), 0)
        self.assertTrue(self.min_stack.is_empty())
        self.assertTrue(self.max_stack.is_empty())
        
        with self.assertRaises(ValueError):
            MonotonicStack(mode="invalid")
        
    def test_push(self):
        self.min_stack.push(5)
        self.assertEqual(len(self.min_stack), 1)
        self.assertFalse(self.min_stack.is_empty())
        
        self.max_stack.push(5)
        self.assertEqual(len(self.max_stack), 1)
        self.assertFalse(self.max_stack.is_empty())
        
    def test_pop(self):
        with self.assertRaises(IndexError):
            self.min_stack.pop()
            
        self.min_stack.push(5)
        self.min_stack.push(3)
        
        value = self.min_stack.pop()
        self.assertEqual(value, 3)
        self.assertEqual(len(self.min_stack), 1)
        
    def test_peek(self):
        with self.assertRaises(IndexError):
            self.min_stack.peek()
            
        self.min_stack.push(5)
        self.min_stack.push(3)
        
        value = self.min_stack.peek()
        self.assertEqual(value, 3)  # LIFO order
        self.assertEqual(len(self.min_stack), 2)  # Ensure stack is unchanged
        
    def test_min_stack(self):
        # Test increasing (min) stack
        values = [5, 3, 7, 4, 8, 1, 9, 2]
        
        for v in values:
            self.min_stack.push(v)
            
        # Current minimum should be 1
        self.assertEqual(self.min_stack.get_min(), 1)
        
        # Pop elements and check minimum updates correctly
        self.min_stack.pop()  # Remove 2
        self.assertEqual(self.min_stack.get_min(), 1)
        
        self.min_stack.pop()  # Remove 9
        self.assertEqual(self.min_stack.get_min(), 1)
        
        self.min_stack.pop()  # Remove 1 (the minimum)
        self.assertEqual(self.min_stack.get_min(), 3)  # New minimum is 3
        
    def test_max_stack(self):
        # Test decreasing (max) stack
        values = [5, 8, 3, 9, 7, 2, 6, 1]
        
        for v in values:
            self.max_stack.push(v)
            
        # Current maximum should be 9
        self.assertEqual(self.max_stack.get_max(), 9)
        
        # Pop elements and check maximum updates correctly
        self.max_stack.pop()  # Remove 1
        self.assertEqual(self.max_stack.get_max(), 9)
        
        self.max_stack.pop()  # Remove 6
        self.assertEqual(self.max_stack.get_max(), 9)
        
        # Pop until removing the maximum
        while self.max_stack.peek() != 9:
            self.max_stack.pop()
        self.max_stack.pop()  # Remove 9 (the maximum)
        self.assertEqual(self.max_stack.get_max(), 8)  # New maximum is 8
        
    def test_monotonic_tracking(self):
        min_stack = MonotonicStack(mode=MonotonicStack.INCREASING)
        
        # Push values with alternating pattern
        min_stack.push(10)
        self.assertEqual(min_stack.get_min(), 10)
        
        min_stack.push(5)
        self.assertEqual(min_stack.get_min(), 5)
        
        min_stack.push(7)
        self.assertEqual(min_stack.get_min(), 5)  # Still 5
        
        min_stack.push(3)
        self.assertEqual(min_stack.get_min(), 3)
        
        # Start popping
        min_stack.pop()  # Remove 3
        self.assertEqual(min_stack.get_min(), 5)
        
        min_stack.pop()  # Remove 7
        self.assertEqual(min_stack.get_min(), 5)
        
        min_stack.pop()  # Remove 5
        self.assertEqual(min_stack.get_min(), 10)
    
    def test_mode_enforcement(self):
        with self.assertRaises(RuntimeError):
            self.max_stack.get_min()  # Wrong mode
            
        with self.assertRaises(RuntimeError):
            self.min_stack.get_max()  # Wrong mode
            
    def test_contains(self):
        self.min_stack.push(5)
        self.min_stack.push(3)
        
        self.assertTrue(5 in self.min_stack)
        self.assertTrue(3 in self.min_stack)
        self.assertFalse(7 in self.min_stack)
        
    def test_clear(self):
        values = [5, 3, 7, 1]
        for v in values:
            self.min_stack.push(v)
            
        self.assertEqual(len(self.min_stack), 4)
        
        self.min_stack.clear()
        self.assertEqual(len(self.min_stack), 0)
        self.assertTrue(self.min_stack.is_empty())
        
        with self.assertRaises(IndexError):
            self.min_stack.get_min()
    
    def test_next_greater_element(self):
        """Test using MonotonicStack to find next greater element"""
        arr = [4, 6, 3, 2, 8, 1, 9, 9, 7]
        next_greater = [-1] * len(arr)
        
        # Use decreasing stack to find next greater element
        stack = []
        
        for i in range(len(arr)):
            # Pop elements from stack while current is greater
            while stack and arr[i] > arr[stack[-1]]:
                idx = stack.pop()
                next_greater[idx] = arr[i]
            
            # Push current index
            stack.append(i)
        
        # Elements still in stack have no next greater element
        expected = [6, 8, 8, 8, 9, 9, -1, -1, -1]
        self.assertEqual(next_greater, expected)

if __name__ == '__main__':
    unittest.main()
