import unittest 

def binary_search(haystack, needle):
    """
    Binary search is a search algorithm that works on O(log n).

    Args:
        - haystack: array of numbers
        - needle: target number

    Returns:
        - (int) index of target number

    """
    left = 0
    right = len(haystack) - 1

    while left <= right:
        middle = left + (right - left) // 2

        if haystack[middle] == needle:
            return middle
        elif haystack[middle] < needle:
            left = middle + 1
        else:
            right = middle - 1 

    return -1


class TestBinarySearch(unittest.TestCase):
    def test_exist(self):
        self.assertEqual(binary_search([1,2,3,4,5], 3), 2)
        self.assertEqual(binary_search([1,2,3,4,5], 1), 0)
        self.assertEqual(binary_search([1,2,3,4,5], 5), 4)

    def test_not_exist(self):
        self.assertEqual(binary_search([1,2,3,4,5], 0), -1)

if __name__ == '__main__':
    unittest.main()


