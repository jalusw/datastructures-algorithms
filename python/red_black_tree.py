import unittest
from typing import Any, Optional

class Node:
    """
    A node in a Red-Black Tree.
    
    Attributes:
        value: The value stored in this node
        left: The left child node
        right: The right child node
        parent: The parent node
        color: The color of the node (True for red, False for black)
    """
    def __init__(self, value: Any):
        self.value = value
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None
        self.color = True  # True for red, False for black

class RedBlackTree:
    """
    A Red-Black Tree is a self-balancing binary search tree with the following properties:
    1. Every node is either red or black
    2. The root is black
    3. All leaves (NIL) are black
    4. If a node is red, then both its children are black
    5. Every path from root to leaves contains the same number of black nodes
    
    Methods:
        - insert(value) add a value to the tree
        - delete(value) remove a value from the tree
        - search(value) check if a value exists
        - get_min() get the minimum value
        - get_max() get the maximum value
        - inorder_traversal() get values in sorted order
    """
    def __init__(self):
        """
        Initialize an empty Red-Black Tree.
        """
        self.root: Optional[Node] = None
        self.nil = Node(None)  # Sentinel node
        self.nil.color = False
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil
        
    def __str__(self) -> str:
        """
        Return the string representation of the tree.
        """
        return f"RedBlackTree(root={self.root.value if self.root else None})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the tree.
        """
        return self.__str__()
        
    def _left_rotate(self, x: Node) -> None:
        """
        Perform a left rotation around node x.
        
        Args:
            x: The node to rotate around
        """
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        
    def _right_rotate(self, x: Node) -> None:
        """
        Perform a right rotation around node x.
        
        Args:
            x: The node to rotate around
        """
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
        
    def _insert_fixup(self, z: Node) -> None:
        """
        Fix the Red-Black Tree properties after insertion.
        
        Args:
            z: The newly inserted node
        """
        while z.parent.color:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color:
                    z.parent.color = False
                    y.color = False
                    z.parent.parent.color = True
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = False
                    z.parent.parent.color = True
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color:
                    z.parent.color = False
                    y.color = False
                    z.parent.parent.color = True
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = False
                    z.parent.parent.color = True
                    self._left_rotate(z.parent.parent)
        self.root.color = False
        
    def _transplant(self, u: Node, v: Node) -> None:
        """
        Replace subtree rooted at u with subtree rooted at v.
        
        Args:
            u: The node to replace
            v: The node to replace with
        """
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
        
    def _delete_fixup(self, x: Node) -> None:
        """
        Fix the Red-Black Tree properties after deletion.
        
        Args:
            x: The node to start fixing from
        """
        while x != self.root and not x.color:
            if x == x.parent.left:
                w = x.parent.right
                if w.color:
                    w.color = False
                    x.parent.color = True
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if not w.left.color and not w.right.color:
                    w.color = True
                    x = x.parent
                else:
                    if not w.right.color:
                        w.left.color = False
                        w.color = True
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = False
                    w.right.color = False
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color:
                    w.color = False
                    x.parent.color = True
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if not w.right.color and not w.left.color:
                    w.color = True
                    x = x.parent
                else:
                    if not w.left.color:
                        w.right.color = False
                        w.color = True
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = False
                    w.left.color = False
                    self._right_rotate(x.parent)
                    x = self.root
        x.color = False
        
    def insert(self, value: Any) -> None:
        """
        Insert a value into the Red-Black Tree.
        
        Args:
            value: The value to insert
        """
        z = Node(value)
        y = self.nil
        x = self.root
        
        # Find the insertion position
        while x != self.nil:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
                
        # Insert the node
        z.parent = y
        if y == self.nil:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z
            
        # Set initial properties
        z.left = self.nil
        z.right = self.nil
        z.color = True
        
        # Fix the tree properties
        self._insert_fixup(z)
        
    def delete(self, value: Any) -> bool:
        """
        Delete a value from the Red-Black Tree.
        
        Args:
            value: The value to delete
            
        Returns:
            True if the value was deleted, False if it wasn't found
        """
        z = self._find_node(value)
        if z == self.nil:
            return False
            
        y = z
        y_original_color = y.color
        
        if z.left == self.nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            
        if not y_original_color:
            self._delete_fixup(x)
            
        return True
        
    def search(self, value: Any) -> bool:
        """
        Check if a value exists in the tree.
        
        Args:
            value: The value to search for
            
        Returns:
            True if the value exists, False otherwise
        """
        return self._find_node(value) != self.nil
        
    def get_min(self) -> Optional[Any]:
        """
        Get the minimum value in the tree.
        
        Returns:
            The minimum value, or None if the tree is empty
        """
        if self.root == self.nil:
            return None
        return self._minimum(self.root).value
        
    def get_max(self) -> Optional[Any]:
        """
        Get the maximum value in the tree.
        
        Returns:
            The maximum value, or None if the tree is empty
        """
        if self.root == self.nil:
            return None
        return self._maximum(self.root).value
        
    def inorder_traversal(self) -> list:
        """
        Get all values in the tree in sorted order.
        
        Returns:
            List of values in sorted order
        """
        result = []
        self._inorder_traversal(self.root, result)
        return result
        
    def _find_node(self, value: Any) -> Node:
        """
        Find a node with the given value.
        
        Args:
            value: The value to find
            
        Returns:
            The node with the value, or self.nil if not found
        """
        current = self.root
        while current != self.nil:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return self.nil
        
    def _minimum(self, node: Node) -> Node:
        """
        Find the minimum value in a subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the minimum value
        """
        while node.left != self.nil:
            node = node.left
        return node
        
    def _maximum(self, node: Node) -> Node:
        """
        Find the maximum value in a subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the maximum value
        """
        while node.right != self.nil:
            node = node.right
        return node
        
    def _inorder_traversal(self, node: Node, result: list) -> None:
        """
        Perform an inorder traversal of the tree.
        
        Args:
            node: The current node
            result: The list to store results
        """
        if node != self.nil:
            self._inorder_traversal(node.left, result)
            result.append(node.value)
            self._inorder_traversal(node.right, result)


class TestRedBlackTree(unittest.TestCase):
    def setUp(self):
        self.tree = RedBlackTree()
        
    def test_init(self):
        self.assertIsNone(self.tree.root)
        self.assertFalse(self.tree.nil.color)
        
    def test_insert(self):
        self.tree.insert(5)
        self.assertEqual(self.tree.root.value, 5)
        self.assertFalse(self.tree.root.color)  # Root should be black
        
        self.tree.insert(3)
        self.tree.insert(7)
        self.assertEqual(self.tree.root.value, 5)
        self.assertEqual(self.tree.root.left.value, 3)
        self.assertEqual(self.tree.root.right.value, 7)
        
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
        
    def test_red_black_properties(self):
        def check_properties(node):
            if node == self.tree.nil:
                return True, 0
                
            # Property 4: If a node is red, both children are black
            if node.color:
                self.assertFalse(node.left.color)
                self.assertFalse(node.right.color)
                
            # Check left and right subtrees
            left_valid, left_black = check_properties(node.left)
            right_valid, right_black = check_properties(node.right)
            
            # Property 5: Every path has same number of black nodes
            self.assertEqual(left_black, right_black)
            
            return left_valid and right_valid, left_black + (0 if node.color else 1)
            
        # Insert some values
        values = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
        for value in values:
            self.tree.insert(value)
            
        # Check all properties
        is_valid, _ = check_properties(self.tree.root)
        self.assertTrue(is_valid)
        self.assertFalse(self.tree.root.color)  # Property 2: Root is black

if __name__ == '__main__':
    unittest.main() 