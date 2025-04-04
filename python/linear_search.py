import unittest

def linear_search(haystack, needle) -> int:
    """
    Linear Search is a brute force algorithm to find a number within an array, takes a list of numbers and number to search,
    returns an index of given number.

    Args:
        - haystack: list of numbers
        - needle: number to find

    Returns:
        index of element 
    """

    for index, value in enumerate(haystack):
        if value == needle:
            return index
    
    return -1


class TestLinearSearch(unittest.TestCase):
    def test_exist(self):
        self.assertEqual(linear_search([1,2,3],1),0)


    def test_not_exists(self):
        self.assertEqual(linear_search([1,2,3],4),-1)


if __name__ == '__main__':
    unittest.main()

