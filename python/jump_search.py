import math
import unittest

def jump_search(haystack: [int], needle: int) -> int:
    length = len(haystack)
    length_sqrt = int(math.sqrt(length))
    step = length_sqrt
    prev = 0

    while prev < length and haystack[min(step,length) - 1] < needle:
        prev = step
        step += length_sqrt

        if prev >= length:
            return -1

    for i in range(prev, min(step, length)):
        if haystack[i] == needle:
            return i

    return -1

class TestJumpSearch(unittest.TestCase):
    def test_exists(self):
        self.assertEqual(jump_search(range(1,100),5), 4)
        self.assertEqual(jump_search(range(1,100),1), 0)
        self.assertEqual(jump_search(range(1,100),50), 49)

    def test_not_exists(self):
        self.assertEqual(jump_search(range(1,100),0), -1)

if __name__ == '__main__':
    unittest.main()

