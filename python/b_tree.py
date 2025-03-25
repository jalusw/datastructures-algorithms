import unittest
from typing import Any, List, Optional, Tuple

class Node:
    """
    A node in a B-Tree.
    
    Attributes:
        keys: List of keys stored in this node
        children: List of child nodes
        leaf: Whether this node is a leaf
        parent: The parent node
    """
    def __init__(self, t: int, leaf: bool = True):
        """
        Initialize a B-Tree node.
        
        Args:
            t: The minimum degree of the B-Tree
            leaf: Whether this node is a leaf
        """
        self.t = t  # Minimum degree
        self.keys: List[Any] = []
        self.children: List[Node] = []
        self.leaf = leaf
        self.parent: Optional[Node] = None

class BTree:
    """
    A B-Tree is a self-balancing tree data structure that maintains sorted data and allows searches,
    sequential access, insertions, and deletions in logarithmic time.
    
    Properties:
    1. Every node has at most 2t children
    2. Every non-leaf node (except root) has at least t children
    3. The root has at least 2 children if it is not a leaf
    4. All leaves appear on the same level
    5. A non-leaf node with k children contains k-1 keys
    
    Methods:
        - insert(value) add a value to the tree
        - delete(value) remove a value from the tree
        - search(value) check if a value exists
        - get_min() get the minimum value
        - get_max() get the maximum value
        - inorder_traversal() get values in sorted order
    """
    def __init__(self, t: int = 2):
        """
        Initialize an empty B-Tree.
        
        Args:
            t: The minimum degree of the B-Tree (default: 2)
        """
        self.root = Node(t)
        self.t = t
        
    def __str__(self) -> str:
        """
        Return the string representation of the tree.
        """
        return f"BTree(t={self.t}, root={self.root.keys if self.root else None})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the tree.
        """
        return self.__str__()
        
    def _split_child(self, x: Node, i: int) -> None:
        """
        Split the child node at index i.
        
        Args:
            x: The parent node
            i: The index of the child to split
        """
        t = self.t
        y = x.children[i]
        z = Node(t, y.leaf)
        z.parent = x
        z.keys = y.keys[t:]
        if not y.leaf:
            z.children = y.children[t:]
            for child in z.children:
                child.parent = z
        x.keys.insert(i, y.keys[t-1])
        x.children.insert(i+1, z)
        y.keys = y.keys[:t-1]
        y.children = y.children[:t]
        
    def _insert_non_full(self, x: Node, k: Any) -> None:
        """
        Insert a key into a non-full node.
        
        Args:
            x: The node to insert into
            k: The key to insert
        """
        i = len(x.keys) - 1
        
        if x.leaf:
            # Insert into leaf node
            while i >= 0 and k < x.keys[i]:
                i -= 1
            x.keys.insert(i + 1, k)
        else:
            # Find child to insert into
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            
            if len(x.children[i].keys) == 2 * self.t - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)
            
    def _merge_children(self, x: Node, i: int) -> None:
        """
        Merge child i with child i+1.
        
        Args:
            x: The parent node
            i: The index of the first child
        """
        y = x.children[i]
        z = x.children[i + 1]
        
        # Merge keys
        y.keys.append(x.keys[i])
        y.keys.extend(z.keys)
        
        # Merge children if not leaves
        if not y.leaf:
            y.children.extend(z.children)
            for child in z.children:
                child.parent = y
                
        # Remove z and the key from x
        x.keys.pop(i)
        x.children.pop(i + 1)
        
    def _borrow_from_next(self, x: Node, i: int) -> None:
        """
        Borrow a key from the next sibling.
        
        Args:
            x: The parent node
            i: The index of the child to borrow for
        """
        y = x.children[i]
        z = x.children[i + 1]
        
        # Move key from x to y
        y.keys.append(x.keys[i])
        x.keys[i] = z.keys.pop(0)
        
        # Move child if not leaves
        if not y.leaf:
            y.children.append(z.children.pop(0))
            y.children[-1].parent = y
            
    def _borrow_from_prev(self, x: Node, i: int) -> None:
        """
        Borrow a key from the previous sibling.
        
        Args:
            x: The parent node
            i: The index of the child to borrow for
        """
        y = x.children[i]
        z = x.children[i - 1]
        
        # Move key from x to y
        y.keys.insert(0, x.keys[i - 1])
        x.keys[i - 1] = z.keys.pop()
        
        # Move child if not leaves
        if not y.leaf:
            y.children.insert(0, z.children.pop())
            y.children[0].parent = y
            
    def _fill(self, x: Node, i: int) -> None:
        """
        Fill a child that has fewer than t-1 keys.
        
        Args:
            x: The parent node
            i: The index of the child to fill
        """
        t = self.t
        
        if i > 0 and len(x.children[i-1].keys) >= t:
            self._borrow_from_prev(x, i)
        elif i < len(x.children) - 1 and len(x.children[i+1].keys) >= t:
            self._borrow_from_next(x, i)
        else:
            if i != len(x.children) - 1:
                self._merge_children(x, i)
            else:
                self._merge_children(x, i-1)
                
    def _remove_from_leaf(self, x: Node, i: int) -> None:
        """
        Remove a key from a leaf node.
        
        Args:
            x: The leaf node
            i: The index of the key to remove
        """
        x.keys.pop(i)
        
    def _remove_from_non_leaf(self, x: Node, i: int) -> None:
        """
        Remove a key from a non-leaf node.
        
        Args:
            x: The non-leaf node
            i: The index of the key to remove
        """
        k = x.keys[i]
        t = self.t
        
        if len(x.children[i].keys) >= t:
            # Find predecessor
            pred = self._get_predecessor(x, i)
            x.keys[i] = pred
            self._delete(x.children[i], pred)
        elif len(x.children[i+1].keys) >= t:
            # Find successor
            succ = self._get_successor(x, i)
            x.keys[i] = succ
            self._delete(x.children[i+1], succ)
        else:
            # Merge children
            self._merge_children(x, i)
            self._delete(x.children[i], k)
            
    def _get_predecessor(self, x: Node, i: int) -> Any:
        """
        Get the predecessor of a key.
        
        Args:
            x: The node containing the key
            i: The index of the key
            
        Returns:
            The predecessor key
        """
        curr = x.children[i]
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.keys[-1]
        
    def _get_successor(self, x: Node, i: int) -> Any:
        """
        Get the successor of a key.
        
        Args:
            x: The node containing the key
            i: The index of the key
            
        Returns:
            The successor key
        """
        curr = x.children[i+1]
        while not curr.leaf:
            curr = curr.children[0]
        return curr.keys[0]
        
    def _find_key(self, k: Any, x: Node) -> Tuple[Optional[Node], int]:
        """
        Find a key in the tree.
        
        Args:
            k: The key to find
            x: The node to start searching from
            
        Returns:
            A tuple of (node, index) if found, (None, -1) otherwise
        """
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return x, i
        if x.leaf:
            return None, -1
        return self._find_key(k, x.children[i])
        
    def _delete(self, x: Node, k: Any) -> None:
        """
        Delete a key from the tree.
        
        Args:
            x: The node to start deletion from
            k: The key to delete
        """
        t = self.t
        i = 0
        
        # Find the key to delete
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
            
        if i < len(x.keys) and k == x.keys[i]:
            if x.leaf:
                self._remove_from_leaf(x, i)
            else:
                self._remove_from_non_leaf(x, i)
        else:
            if x.leaf:
                return  # Key not found
                
            # If the last child has fewer than t keys
            if len(x.children[i].keys) < t:
                self._fill(x, i)
                
            # If the last merge caused the root to become empty
            if i > len(x.keys):
                i -= 1
                
            self._delete(x.children[i], k)
            
    def insert(self, k: Any) -> None:
        """
        Insert a key into the B-Tree.
        
        Args:
            k: The key to insert
        """
        root = self.root
        
        # If root is full, create new root
        if len(root.keys) == 2 * self.t - 1:
            temp = Node(self.t, False)
            self.root = temp
            temp.children.append(root)
            root.parent = temp
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)
            
    def delete(self, k: Any) -> bool:
        """
        Delete a key from the B-Tree.
        
        Args:
            k: The key to delete
            
        Returns:
            True if the key was deleted, False if it wasn't found
        """
        root = self.root
        
        # If tree is empty
        if not root:
            return False
            
        # If root has no keys
        if len(root.keys) == 0:
            if root.children:
                self.root = root.children[0]
                self.root.parent = None
            else:
                self.root = Node(self.t)
            return True
            
        # Delete the key
        self._delete(root, k)
        
        # If root has no keys and has a child
        if len(root.keys) == 0 and root.children:
            self.root = root.children[0]
            self.root.parent = None
            
        return True
        
    def search(self, k: Any) -> bool:
        """
        Search for a key in the B-Tree.
        
        Args:
            k: The key to search for
            
        Returns:
            True if the key exists, False otherwise
        """
        node, _ = self._find_key(k, self.root)
        return node is not None
        
    def get_min(self) -> Optional[Any]:
        """
        Get the minimum key in the B-Tree.
        
        Returns:
            The minimum key, or None if the tree is empty
        """
        if not self.root or not self.root.keys:
            return None
            
        curr = self.root
        while not curr.leaf:
            curr = curr.children[0]
        return curr.keys[0]
        
    def get_max(self) -> Optional[Any]:
        """
        Get the maximum key in the B-Tree.
        
        Returns:
            The maximum key, or None if the tree is empty
        """
        if not self.root or not self.root.keys:
            return None
            
        curr = self.root
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.keys[-1]
        
    def inorder_traversal(self) -> List[Any]:
        """
        Get all keys in the B-Tree in sorted order.
        
        Returns:
            List of keys in sorted order
        """
        result = []
        self._inorder_traversal(self.root, result)
        return result
        
    def _inorder_traversal(self, x: Node, result: List[Any]) -> None:
        """
        Perform an inorder traversal of the B-Tree.
        
        Args:
            x: The current node
            result: The list to store results
        """
        i = 0
        for i in range(len(x.keys)):
            if not x.leaf:
                self._inorder_traversal(x.children[i], result)
            result.append(x.keys[i])
        if not x.leaf:
            self._inorder_traversal(x.children[i+1], result)


class TestBTree(unittest.TestCase):
    def setUp(self):
        self.tree = BTree(t=2)
        
    def test_init(self):
        self.assertEqual(self.tree.t, 2)
        self.assertTrue(self.tree.root.leaf)
        self.assertEqual(len(self.tree.root.keys), 0)
        
    def test_insert(self):
        self.tree.insert(5)
        self.assertEqual(self.tree.root.keys, [5])
        
        self.tree.insert(3)
        self.tree.insert(7)
        self.assertEqual(self.tree.root.keys, [5])
        self.assertEqual(self.tree.root.children[0].keys, [3])
        self.assertEqual(self.tree.root.children[1].keys, [7])
        
    def test_search(self):
        self.tree.insert(5)
        self.tree.insert(3)
        self.tree.insert(7)
        
        self.assertTrue(self.tree.search(5))
        self.assertTrue(self.tree.search(3))
        self.assertTrue(self.tree.search(7))
        self.assertFalse(self.tree.search(4))
        self.assertFalse(self.tree.search(6))
        
    def test_delete(self):
        self.tree.insert(5)
        self.tree.insert(3)
        self.tree.insert(7)
        
        self.assertTrue(self.tree.delete(3))
        self.assertFalse(self.tree.search(3))
        self.assertTrue(self.tree.search(5))
        self.assertTrue(self.tree.search(7))
        
        self.assertTrue(self.tree.delete(5))
        self.assertFalse(self.tree.search(5))
        self.assertTrue(self.tree.search(7))
        
    def test_get_min_max(self):
        self.tree.insert(5)
        self.tree.insert(3)
        self.tree.insert(7)
        self.tree.insert(1)
        self.tree.insert(9)
        
        self.assertEqual(self.tree.get_min(), 1)
        self.assertEqual(self.tree.get_max(), 9)
        
    def test_inorder_traversal(self):
        values = [5, 3, 7, 1, 9, 4, 6, 8]
        for value in values:
            self.tree.insert(value)
            
        expected = sorted(values)
        self.assertEqual(self.tree.inorder_traversal(), expected)
        
    def test_empty_tree(self):
        self.assertIsNone(self.tree.get_min())
        self.assertIsNone(self.tree.get_max())
        self.assertEqual(self.tree.inorder_traversal(), [])
        self.assertFalse(self.tree.search(5))
        self.assertFalse(self.tree.delete(5))
        
    def test_duplicate_values(self):
        self.tree.insert(5)
        self.tree.insert(5)
        self.assertEqual(len(self.tree.inorder_traversal()), 2)
        
    def test_complex_operations(self):
        # Insert a sequence of values
        values = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
        for value in values:
            self.tree.insert(value)
            
        # Verify initial state
        self.assertEqual(self.tree.inorder_traversal(), sorted(values))
        
        # Delete some values
        self.assertTrue(self.tree.delete(18))
        self.assertTrue(self.tree.delete(11))
        self.assertTrue(self.tree.delete(3))
        
        # Verify final state
        remaining = [7, 10, 22, 8, 26, 2, 6, 13]
        self.assertEqual(self.tree.inorder_traversal(), sorted(remaining))
        
    def test_b_tree_properties(self):
        def check_properties(node):
            if node.leaf:
                return True
                
            # Property 1: Every node has at most 2t children
            self.assertLessEqual(len(node.children), 2 * self.tree.t)
            
            # Property 2: Every non-leaf node has at least t children
            self.assertGreaterEqual(len(node.children), self.tree.t)
            
            # Property 3: Root has at least 2 children if not a leaf
            if node == self.tree.root:
                self.assertGreaterEqual(len(node.children), 2)
                
            # Property 4: All leaves are at the same level
            if not node.leaf:
                leaf_levels = set()
                for child in node.children:
                    if child.leaf:
                        leaf_levels.add(0)
                    else:
                        leaf_levels.update(level + 1 for level in check_properties(child))
                self.assertEqual(len(leaf_levels), 1)
                return leaf_levels
                
            return {0}
            
        # Insert some values
        values = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
        for value in values:
            self.tree.insert(value)
            
        # Check all properties
        check_properties(self.tree.root)

if __name__ == '__main__':
    unittest.main() 