import unittest

class Array:
    """
    Array is a data structure, providing a way to store multiple values.
    
    Methods:
        - append(value) append value to the array
        - remove(index) remove value at specified index
    """
    def __init__(self) -> None:
        """
        Initialize the array.
        """
        self.items = []

    def __str__(self) -> str:
        """
        Return the string representation of the array.
        """
        return f"{self.items}"

    def __repr__(self) -> str:
        """
        Return the string representation of the array. 
        """
        return f"Array({self.items})"

    def __len__(self) -> int:
        """
        Return the length of the array.
        """
        return len(self.items)

    def __contains__(self, value) -> bool:
        """
        Check if the value is in the array.
        
        Args:
            value: the value to check
        """
        return value in self.items

    def __getitem__(self, index) -> int:
        """
        Return the value at the specified index.

        Args:
            index: the index of the value to return

        Raises:
            IndexError: if the index is out of range
        """
        if index > self.__len__():
            raise IndexError("Index out of range")
        return self.items[index]

    def append(self, value) -> None:
        """
        Append the value to the array.

        Args:
            value: the value to append
        """

        return self.items.append(value)

    def remove(self, index) -> None:
        """
        Remove the value at the specified index.
        
        Args:
            index: the index of the value to remove
        
        Raises:
            IndexError: if the index is out of range
        """

        if index >= self.__len__():
            raise IndexError("Index out of range")
        del self.items[index]

class TestArray(unittest.TestCase):
    def setUp(self):
        self.array = Array()

    def test_init(self):
        self.assertEqual(self.array.items, [])
        self.assertEqual(len(self.array), 0)

    def test_append(self):
        self.array.append(7)

        self.assertEqual(self.array.items, [7])
        self.assertEqual(len(self.array), 1)

    def test_remove(self):
        self.array.append(8)
        self.array.append(9)

        self.array.remove(1)

        self.assertEqual(self.array.items, [8])
        self.assertEqual(len(self.array), 1)

        with self.assertRaises(IndexError):
            self.array.remove(4)

    def test_lookup(self):
        self.array.append(1)
        self.array.append(2)

        self.assertEqual(self.array[1], 2)

        with self.assertRaises(IndexError):
            self.array[100]

    def test_contain(self):
        self.array.append(1)
        self.array.append(3)
        self.assertEqual(2 in self.array, False)
        self.assertEqual(1 in self.array, True)

if __name__ == '__main__':
    unittest.main()
