import unittest
from typing import Any, Dict, List, Optional, Set

class DisjointSet:
    """
    A Disjoint Set (Union-Find) data structure that efficiently tracks a partition
    of a set into disjoint subsets. It supports two main operations:
    - find: determine which subset a particular element is in
    - union: join two subsets into a single subset
    
    This implementation uses path compression and union by rank optimizations
    to achieve near-constant time complexity for operations.
    
    Methods:
        - make_set(value) create a new set containing a single element
        - find(value) find the representative of the set containing an element
        - union(value1, value2) merge the sets containing two elements
        - is_connected(value1, value2) check if two elements are in the same set
        - get_set_size(value) get the size of the set containing an element
        - get_sets() get all disjoint sets
    """
    def __init__(self):
        """
        Initialize an empty disjoint set.
        """
        self.parent: Dict[Any, Any] = {}  # Maps elements to their parent
        self.rank: Dict[Any, int] = {}     # Maps elements to their rank
        self.size: Dict[Any, int] = {}     # Maps representatives to set sizes
        
    def __str__(self) -> str:
        """
        Return the string representation of the disjoint set.
        """
        return f"DisjointSet(sets={len(self.get_sets())})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the disjoint set.
        """
        return self.__str__()
        
    def make_set(self, value: Any) -> None:
        """
        Create a new set containing a single element.
        
        Args:
            value: The element to create a set for
        """
        if value not in self.parent:
            self.parent[value] = value
            self.rank[value] = 0
            self.size[value] = 1
            
    def find(self, value: Any) -> Optional[Any]:
        """
        Find the representative of the set containing an element.
        Uses path compression for optimization.
        
        Args:
            value: The element to find the representative for
            
        Returns:
            The representative of the set containing the element, or None if not found
        """
        if value not in self.parent:
            return None
            
        # Path compression
        if self.parent[value] != value:
            self.parent[value] = self.find(self.parent[value])
        return self.parent[value]
        
    def union(self, value1: Any, value2: Any) -> bool:
        """
        Merge the sets containing two elements.
        Uses union by rank for optimization.
        
        Args:
            value1: The first element
            value2: The second element
            
        Returns:
            True if the sets were merged, False if they were already in the same set
        """
        root1 = self.find(value1)
        root2 = self.find(value2)
        
        if root1 is None or root2 is None:
            return False
            
        if root1 == root2:
            return False
            
        # Union by rank
        if self.rank[root1] < self.rank[root2]:
            root1, root2 = root2, root1
            
        self.parent[root2] = root1
        self.size[root1] += self.size[root2]
        
        if self.rank[root1] == self.rank[root2]:
            self.rank[root1] += 1
            
        return True
        
    def is_connected(self, value1: Any, value2: Any) -> bool:
        """
        Check if two elements are in the same set.
        
        Args:
            value1: The first element
            value2: The second element
            
        Returns:
            True if the elements are in the same set, False otherwise
        """
        root1 = self.find(value1)
        root2 = self.find(value2)
        return root1 is not None and root2 is not None and root1 == root2
        
    def get_set_size(self, value: Any) -> Optional[int]:
        """
        Get the size of the set containing an element.
        
        Args:
            value: The element to get the set size for
            
        Returns:
            The size of the set containing the element, or None if not found
        """
        root = self.find(value)
        return self.size.get(root)
        
    def get_sets(self) -> List[Set[Any]]:
        """
        Get all disjoint sets.
        
        Returns:
            List of sets, where each set contains the elements in that subset
        """
        # Group elements by their representative
        sets: Dict[Any, Set[Any]] = {}
        for value in self.parent:
            root = self.find(value)
            if root not in sets:
                sets[root] = set()
            sets[root].add(value)
        return list(sets.values())
        
    def clear(self) -> None:
        """
        Remove all sets from the disjoint set.
        """
        self.parent.clear()
        self.rank.clear()
        self.size.clear()


class TestDisjointSet(unittest.TestCase):
    def setUp(self):
        self.ds = DisjointSet()
        
    def test_init(self):
        self.assertEqual(len(self.ds.parent), 0)
        self.assertEqual(len(self.ds.rank), 0)
        self.assertEqual(len(self.ds.size), 0)
        
    def test_make_set(self):
        self.ds.make_set("A")
        self.assertEqual(self.ds.parent["A"], "A")
        self.assertEqual(self.ds.rank["A"], 0)
        self.assertEqual(self.ds.size["A"], 1)
        
        # Test making set for existing element
        self.ds.make_set("A")
        self.assertEqual(self.ds.parent["A"], "A")
        self.assertEqual(self.ds.rank["A"], 0)
        self.assertEqual(self.ds.size["A"], 1)
        
    def test_find(self):
        self.ds.make_set("A")
        self.ds.make_set("B")
        self.ds.make_set("C")
        
        self.assertEqual(self.ds.find("A"), "A")
        self.assertEqual(self.ds.find("B"), "B")
        self.assertEqual(self.ds.find("C"), "C")
        self.assertIsNone(self.ds.find("D"))
        
    def test_union(self):
        self.ds.make_set("A")
        self.ds.make_set("B")
        self.ds.make_set("C")
        
        # Test successful union
        self.assertTrue(self.ds.union("A", "B"))
        self.assertEqual(self.ds.find("A"), self.ds.find("B"))
        self.assertEqual(self.ds.get_set_size("A"), 2)
        
        # Test union of already connected elements
        self.assertFalse(self.ds.union("A", "B"))
        
        # Test union with non-existent element
        self.assertFalse(self.ds.union("A", "D"))
        
    def test_is_connected(self):
        self.ds.make_set("A")
        self.ds.make_set("B")
        self.ds.make_set("C")
        
        self.assertFalse(self.ds.is_connected("A", "B"))
        self.assertFalse(self.ds.is_connected("B", "C"))
        self.assertFalse(self.ds.is_connected("A", "C"))
        
        self.ds.union("A", "B")
        self.assertTrue(self.ds.is_connected("A", "B"))
        self.assertFalse(self.ds.is_connected("B", "C"))
        self.assertFalse(self.ds.is_connected("A", "C"))
        
        self.ds.union("B", "C")
        self.assertTrue(self.ds.is_connected("A", "B"))
        self.assertTrue(self.ds.is_connected("B", "C"))
        self.assertTrue(self.ds.is_connected("A", "C"))
        
    def test_get_set_size(self):
        self.ds.make_set("A")
        self.ds.make_set("B")
        self.ds.make_set("C")
        
        self.assertEqual(self.ds.get_set_size("A"), 1)
        self.assertEqual(self.ds.get_set_size("B"), 1)
        self.assertEqual(self.ds.get_set_size("C"), 1)
        
        self.ds.union("A", "B")
        self.assertEqual(self.ds.get_set_size("A"), 2)
        self.assertEqual(self.ds.get_set_size("B"), 2)
        self.assertEqual(self.ds.get_set_size("C"), 1)
        
        self.ds.union("B", "C")
        self.assertEqual(self.ds.get_set_size("A"), 3)
        self.assertEqual(self.ds.get_set_size("B"), 3)
        self.assertEqual(self.ds.get_set_size("C"), 3)
        
        self.assertIsNone(self.ds.get_set_size("D"))
        
    def test_get_sets(self):
        self.ds.make_set("A")
        self.ds.make_set("B")
        self.ds.make_set("C")
        self.ds.make_set("D")
        
        initial_sets = self.ds.get_sets()
        self.assertEqual(len(initial_sets), 4)
        self.assertEqual(set(s for s in initial_sets), {
            {"A"}, {"B"}, {"C"}, {"D"}
        })
        
        self.ds.union("A", "B")
        self.ds.union("C", "D")
        
        merged_sets = self.ds.get_sets()
        self.assertEqual(len(merged_sets), 2)
        self.assertEqual(set(s for s in merged_sets), {
            {"A", "B"}, {"C", "D"}
        })
        
    def test_clear(self):
        self.ds.make_set("A")
        self.ds.make_set("B")
        self.ds.union("A", "B")
        
        self.ds.clear()
        self.assertEqual(len(self.ds.parent), 0)
        self.assertEqual(len(self.ds.rank), 0)
        self.assertEqual(len(self.ds.size), 0)
        
    def test_path_compression(self):
        # Create a chain A -> B -> C -> D
        self.ds.make_set("A")
        self.ds.make_set("B")
        self.ds.make_set("C")
        self.ds.make_set("D")
        
        self.ds.parent["B"] = "A"
        self.ds.parent["C"] = "B"
        self.ds.parent["D"] = "C"
        
        # Find should compress the path
        self.assertEqual(self.ds.find("D"), "A")
        self.assertEqual(self.ds.parent["D"], "A")
        self.assertEqual(self.ds.parent["C"], "A")
        self.assertEqual(self.ds.parent["B"], "A")
        
    def test_union_by_rank(self):
        # Create two trees with different ranks
        self.ds.make_set("A")
        self.ds.make_set("B")
        self.ds.make_set("C")
        self.ds.make_set("D")
        
        self.ds.parent["B"] = "A"
        self.ds.rank["A"] = 1
        
        self.ds.parent["D"] = "C"
        self.ds.rank["C"] = 0
        
        # Union should attach the lower rank tree to the higher rank tree
        self.ds.union("A", "C")
        self.assertEqual(self.ds.find("D"), "A")
        self.assertEqual(self.ds.rank["A"], 1)
        
    def test_complex_operations(self):
        # Create multiple sets and perform various operations
        for i in range(10):
            self.ds.make_set(i)
            
        # Union some sets
        self.ds.union(0, 1)
        self.ds.union(2, 3)
        self.ds.union(4, 5)
        self.ds.union(6, 7)
        self.ds.union(8, 9)
        
        # Check set sizes
        self.assertEqual(self.ds.get_set_size(0), 2)
        self.assertEqual(self.ds.get_set_size(2), 2)
        self.assertEqual(self.ds.get_set_size(4), 2)
        self.assertEqual(self.ds.get_set_size(6), 2)
        self.assertEqual(self.ds.get_set_size(8), 2)
        
        # Union more sets
        self.ds.union(1, 3)
        self.ds.union(5, 7)
        
        # Check updated set sizes
        self.assertEqual(self.ds.get_set_size(0), 4)
        self.assertEqual(self.ds.get_set_size(4), 4)
        self.assertEqual(self.ds.get_set_size(8), 2)
        
        # Check connectivity
        self.assertTrue(self.ds.is_connected(0, 3))
        self.assertTrue(self.ds.is_connected(4, 7))
        self.assertFalse(self.ds.is_connected(0, 4))
        self.assertFalse(self.ds.is_connected(0, 8))
        
        # Get all sets
        sets = self.ds.get_sets()
        self.assertEqual(len(sets), 3)
        self.assertEqual(set(s for s in sets), {
            {0, 1, 2, 3},
            {4, 5, 6, 7},
            {8, 9}
        })


if __name__ == '__main__':
    unittest.main() 