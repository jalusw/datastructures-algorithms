import unittest
from typing import Any, Optional, List

class Node:
    """
    A node in a binary search tree.
    
    Attributes:
        value: The value stored in the node
        left: Reference to the left child node
        right: Reference to the right child node
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    """
    BinarySearchTree is a binary tree data structure where:
    - The left subtree of a node contains only nodes with values less than the node's value
    - The right subtree of a node contains only nodes with values greater than the node's value
    - Both the left and right subtrees are also binary search trees
    
    Methods:
        - insert(value): Insert a value into the tree
        - search(value): Search for a value in the tree
        - delete(value): Delete a value from the tree
        - min(): Find the minimum value in the tree
        - max(): Find the maximum value in the tree
        - inorder_traversal(): Return values in sorted order
        - preorder_traversal(): Return values in preorder
        - postorder_traversal(): Return values in postorder
    """
    def __init__(self):
        """
        Initialize an empty binary search tree.
        """
        self.root = None
        self.size = 0
        
    def __str__(self) -> str:
        """
        Return the string representation of the tree.
        """
        if not self.root:
            return "[]"
        
        values = self.inorder_traversal()
        return f"{values}"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the tree.
        """
        return f"BinarySearchTree({self.__str__()})"
        
    def __len__(self) -> int:
        """
        Return the number of nodes in the tree.
        """
        return self.size
        
    def __contains__(self, value) -> bool:
        """
        Check if the value is in the tree.
        
        Args:
            value: The value to check
        """
        return self.search(value)
        
    def _insert_recursive(self, node: Optional[Node], value: Any) -> Node:
        """
        Recursively insert a value into the tree.
        
        Args:
            node: The current node
            value: The value to insert
            
        Returns:
            The root node of the subtree
        """
        if node is None:
            self.size += 1
            return Node(value)
            
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        # If value is equal to node.value, do nothing (no duplicates)
            
        return node
        
    def insert(self, value: Any) -> None:
        """
        Insert a value into the tree.
        
        Args:
            value: The value to insert
        """
        self.root = self._insert_recursive(self.root, value)
        
    def _search_recursive(self, node: Optional[Node], value: Any) -> bool:
        """
        Recursively search for a value in the tree.
        
        Args:
            node: The current node
            value: The value to search for
            
        Returns:
            True if found, False otherwise
        """
        if node is None:
            return False
            
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
            
    def search(self, value: Any) -> bool:
        """
        Search for a value in the tree.
        
        Args:
            value: The value to search for
            
        Returns:
            True if found, False otherwise
        """
        return self._search_recursive(self.root, value)
        
    def _find_min(self, node: Node) -> Node:
        """
        Find the minimum value in the subtree rooted at node.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the minimum value
        """
        current = node
        while current.left:
            current = current.left
        return current
        
    def _delete_recursive(self, node: Optional[Node], value: Any) -> Optional[Node]:
        """
        Recursively delete a value from the tree.
        
        Args:
            node: The current node
            value: The value to delete
            
        Returns:
            The root node of the modified subtree
        """
        if node is None:
            return None
            
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node found, delete it
            
            # Case 1: Leaf node (no children)
            if node.left is None and node.right is None:
                self.size -= 1
                return None
                
            # Case 2: Node with only one child
            elif node.left is None:
                self.size -= 1
                return node.right
            elif node.right is None:
                self.size -= 1
                return node.left
                
            # Case 3: Node with two children
            # Find the inorder successor (smallest value in right subtree)
            successor = self._find_min(node.right)
            # Copy the successor's value to this node
            node.value = successor.value
            # Delete the successor
            node.right = self._delete_recursive(node.right, successor.value)
            
        return node
        
    def delete(self, value: Any) -> None:
        """
        Delete a value from the tree.
        
        Args:
            value: The value to delete
        """
        self.root = self._delete_recursive(self.root, value)
        
    def min(self) -> Any:
        """
        Find the minimum value in the tree.
        
        Returns:
            The minimum value
            
        Raises:
            ValueError: If the tree is empty
        """
        if not self.root:
            raise ValueError("Cannot find minimum in an empty tree")
            
        min_node = self._find_min(self.root)
        return min_node.value
        
    def _find_max(self, node: Node) -> Node:
        """
        Find the maximum value in the subtree rooted at node.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the maximum value
        """
        current = node
        while current.right:
            current = current.right
        return current
        
    def max(self) -> Any:
        """
        Find the maximum value in the tree.
        
        Returns:
            The maximum value
            
        Raises:
            ValueError: If the tree is empty
        """
        if not self.root:
            raise ValueError("Cannot find maximum in an empty tree")
            
        max_node = self._find_max(self.root)
        return max_node.value
        
    def _inorder_traversal_recursive(self, node: Optional[Node], result: List[Any]) -> None:
        """
        Recursively traverse the tree in inorder.
        
        Args:
            node: The current node
            result: The list to store values
        """
        if node:
            self._inorder_traversal_recursive(node.left, result)
            result.append(node.value)
            self._inorder_traversal_recursive(node.right, result)
            
    def inorder_traversal(self) -> List[Any]:
        """
        Traverse the tree in inorder (left, root, right).
        
        Returns:
            List of values in inorder traversal
        """
        result = []
        self._inorder_traversal_recursive(self.root, result)
        return result
        
    def _preorder_traversal_recursive(self, node: Optional[Node], result: List[Any]) -> None:
        """
        Recursively traverse the tree in preorder.
        
        Args:
            node: The current node
            result: The list to store values
        """
        if node:
            result.append(node.value)
            self._preorder_traversal_recursive(node.left, result)
            self._preorder_traversal_recursive(node.right, result)
            
    def preorder_traversal(self) -> List[Any]:
        """
        Traverse the tree in preorder (root, left, right).
        
        Returns:
            List of values in preorder traversal
        """
        result = []
        self._preorder_traversal_recursive(self.root, result)
        return result
        
    def _postorder_traversal_recursive(self, node: Optional[Node], result: List[Any]) -> None:
        """
        Recursively traverse the tree in postorder.
        
        Args:
            node: The current node
            result: The list to store values
        """
        if node:
            self._postorder_traversal_recursive(node.left, result)
            self._postorder_traversal_recursive(node.right, result)
            result.append(node.value)
            
    def postorder_traversal(self) -> List[Any]:
        """
        Traverse the tree in postorder (left, right, root).
        
        Returns:
            List of values in postorder traversal
        """
        result = []
        self._postorder_traversal_recursive(self.root, result)
        return result
        
    def is_empty(self) -> bool:
        """
        Check if the tree is empty.
        
        Returns:
            True if the tree is empty, False otherwise
        """
        return self.root is None
        
    def clear(self) -> None:
        """
        Remove all elements from the tree.
        """
        self.root = None
        self.size = 0
        
    def height(self) -> int:
        """
        Calculate the height of the tree.
        
        Returns:
            The height of the tree
        """
        def _height_recursive(node):
            if node is None:
                return 0
            return 1 + max(_height_recursive(node.left), _height_recursive(node.right))
            
        return _height_recursive(self.root)


class TestBinarySearchTree(unittest.TestCase):
    def setUp(self):
        self.bst = BinarySearchTree()
        
    def test_init(self):
        self.assertIsNone(self.bst.root)
        self.assertEqual(len(self.bst), 0)
        self.assertTrue(self.bst.is_empty())
        
    def test_insert(self):
        self.bst.insert(5)
        self.assertEqual(self.bst.root.value, 5)
        self.assertEqual(len(self.bst), 1)
        self.assertFalse(self.bst.is_empty())
        
        self.bst.insert(3)
        self.bst.insert(7)
        self.assertEqual(len(self.bst), 3)
        self.assertEqual(self.bst.root.left.value, 3)
        self.assertEqual(self.bst.root.right.value, 7)
        
        # Test inserting duplicates (should not change the size)
        self.bst.insert(5)
        self.assertEqual(len(self.bst), 3)
        
    def test_search(self):
        self.bst.insert(5)
        self.bst.insert(3)
        self.bst.insert(7)
        
        self.assertTrue(self.bst.search(5))
        self.assertTrue(self.bst.search(3))
        self.assertTrue(self.bst.search(7))
        self.assertFalse(self.bst.search(10))
        
        # Test __contains__
        self.assertTrue(5 in self.bst)
        self.assertFalse(10 in self.bst)
        
    def test_delete(self):
        # Test deleting from empty tree
        self.bst.delete(5)  # Should not raise an error
        
        # Insert elements
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.bst.insert(value)
            
        # Test case 1: Delete leaf node
        self.bst.delete(2)
        self.assertEqual(len(self.bst), 6)
        self.assertFalse(2 in self.bst)
        
        # Test case 2: Delete node with one child
        self.bst.delete(3)
        self.assertEqual(len(self.bst), 5)
        self.assertFalse(3 in self.bst)
        self.assertTrue(4 in self.bst)  # Child should still be there
        
        # Test case 3: Delete node with two children
        self.bst.delete(7)
        self.assertEqual(len(self.bst), 4)
        self.assertFalse(7 in self.bst)
        self.assertTrue(6 in self.bst)  # Children should still be there
        self.assertTrue(8 in self.bst)
        
        # Test deleting root
        self.bst.delete(5)
        self.assertEqual(len(self.bst), 3)
        self.assertFalse(5 in self.bst)
        
    def test_min_max(self):
        with self.assertRaises(ValueError):
            self.bst.min()  # Empty tree
            
        with self.assertRaises(ValueError):
            self.bst.max()  # Empty tree
            
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.bst.insert(value)
            
        self.assertEqual(self.bst.min(), 2)
        self.assertEqual(self.bst.max(), 8)
        
        # After deleting min
        self.bst.delete(2)
        self.assertEqual(self.bst.min(), 3)
        
        # After deleting max
        self.bst.delete(8)
        self.assertEqual(self.bst.max(), 7)
        
    def test_traversals(self):
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.bst.insert(value)
            
        # Inorder should be sorted
        self.assertEqual(self.bst.inorder_traversal(), [2, 3, 4, 5, 6, 7, 8])
        
        # Preorder: root, left, right
        self.assertEqual(self.bst.preorder_traversal(), [5, 3, 2, 4, 7, 6, 8])
        
        # Postorder: left, right, root
        self.assertEqual(self.bst.postorder_traversal(), [2, 4, 3, 6, 8, 7, 5])
        
    def test_clear(self):
        values = [5, 3, 7, 2, 4, 6, 8]
        for value in values:
            self.bst.insert(value)
            
        self.assertEqual(len(self.bst), 7)
        
        self.bst.clear()
        self.assertEqual(len(self.bst), 0)
        self.assertTrue(self.bst.is_empty())
        self.assertIsNone(self.bst.root)
        
    def test_height(self):
        self.assertEqual(self.bst.height(), 0)  # Empty tree
        
        self.bst.insert(5)
        self.assertEqual(self.bst.height(), 1)  # Just root
        
        self.bst.insert(3)
        self.assertEqual(self.bst.height(), 2)  # Root and one child
        
        # Build a balanced tree
        values = [5, 3, 7, 2, 4, 6, 8]
        self.bst.clear()
        for value in values:
            self.bst.insert(value)
            
        self.assertEqual(self.bst.height(), 3)  # Balanced tree height
        
        # Build an unbalanced tree
        self.bst.clear()
        for i in range(1, 6):
            self.bst.insert(i)  # Right-leaning tree: 1->2->3->4->5
            
        self.assertEqual(self.bst.height(), 5)  # Linear tree

if __name__ == '__main__':
    unittest.main()
