import unittest
from typing import Any, Optional, List, Tuple

class Node:
    """
    A node in an AVL tree.
    
    Attributes:
        value: The value stored in the node
        left: Reference to the left child node
        right: Reference to the right child node
        height: The height of the subtree rooted at this node
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1  # Height of a new node is 1

class AVLTree:
    """
    AVLTree is a self-balancing binary search tree where the heights of the
    two child subtrees of any node differ by at most one.
    
    Methods:
        - insert(value): Insert a value into the tree while maintaining balance
        - delete(value): Delete a value from the tree while maintaining balance
        - search(value): Search for a value in the tree
        - get_min(): Find the minimum value in the tree
        - get_max(): Find the maximum value in the tree
        - inorder_traversal(): Return values in sorted order
        - get_balance_factor(node): Get the balance factor of a node
    """
    def __init__(self):
        """
        Initialize an empty AVL tree.
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
        return f"AVLTree({self.__str__()})"
        
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
    
    def _get_height(self, node: Optional[Node]) -> int:
        """
        Get the height of a node.
        
        Args:
            node: The node
            
        Returns:
            The height of the node, or 0 if the node is None
        """
        if node is None:
            return 0
        return node.height
    
    def _get_balance_factor(self, node: Optional[Node]) -> int:
        """
        Get the balance factor of a node.
        The balance factor is the height of the left subtree minus
        the height of the right subtree.
        
        Args:
            node: The node
            
        Returns:
            The balance factor, or 0 if the node is None
        """
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def _right_rotate(self, y: Node) -> Node:
        """
        Perform a right rotation on the given node.
        
        Args:
            y: The node to rotate
            
        Returns:
            The new root of the subtree after rotation
        """
        x = y.left
        T2 = x.right
        
        # Perform rotation
        x.right = y
        y.left = T2
        
        # Update heights
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        
        return x
    
    def _left_rotate(self, x: Node) -> Node:
        """
        Perform a left rotation on the given node.
        
        Args:
            x: The node to rotate
            
        Returns:
            The new root of the subtree after rotation
        """
        y = x.right
        T2 = y.left
        
        # Perform rotation
        y.left = x
        x.right = T2
        
        # Update heights
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        
        return y
    
    def _insert_recursive(self, node: Optional[Node], value: Any) -> Node:
        """
        Recursively insert a value into the tree.
        
        Args:
            node: The current node
            value: The value to insert
            
        Returns:
            The root node of the balanced subtree
        """
        # Standard BST insertion
        if node is None:
            self.size += 1
            return Node(value)
            
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            # Duplicate value, ignore
            return node
            
        # Update height of this ancestor node
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1
        
        # Get the balance factor to check if the node became unbalanced
        balance = self._get_balance_factor(node)
        
        # Left Left Case
        if balance > 1 and (value < node.left.value if node.left else False):
            return self._right_rotate(node)
            
        # Right Right Case
        if balance < -1 and (value > node.right.value if node.right else False):
            return self._left_rotate(node)
            
        # Left Right Case
        if balance > 1 and (value > node.left.value if node.left else False):
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
            
        # Right Left Case
        if balance < -1 and (value < node.right.value if node.right else False):
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
            
        return node
    
    def insert(self, value: Any) -> None:
        """
        Insert a value into the tree.
        
        Args:
            value: The value to insert
        """
        self.root = self._insert_recursive(self.root, value)
    
    def _find_min_node(self, node: Node) -> Node:
        """
        Find the node with the minimum value in the subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The node with the minimum value
        """
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def _delete_recursive(self, node: Optional[Node], value: Any) -> Optional[Node]:
        """
        Recursively delete a value from the tree.
        
        Args:
            node: The current node
            value: The value to delete
            
        Returns:
            The root node of the balanced subtree
        """
        # Standard BST deletion
        if node is None:
            return None
            
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node with the value to be deleted found
            
            # Case 1: Node with only one child or no child
            if node.left is None:
                temp = node.right
                node = None
                self.size -= 1
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                self.size -= 1
                return temp
                
            # Case 2: Node with two children
            # Get the inorder successor (smallest in the right subtree)
            temp = self._find_min_node(node.right)
            
            # Copy the inorder successor's value to this node
            node.value = temp.value
            
            # Delete the inorder successor
            node.right = self._delete_recursive(node.right, temp.value)
            
        # If the tree had only one node, return
        if node is None:
            return None
            
        # Update height of the current node
        node.height = max(self._get_height(node.left), self._get_height(node.right)) + 1
        
        # Get the balance factor to check if the node became unbalanced
        balance = self._get_balance_factor(node)
        
        # Left Left Case
        if balance > 1 and self._get_balance_factor(node.left) >= 0:
            return self._right_rotate(node)
            
        # Left Right Case
        if balance > 1 and self._get_balance_factor(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
            
        # Right Right Case
        if balance < -1 and self._get_balance_factor(node.right) <= 0:
            return self._left_rotate(node)
            
        # Right Left Case
        if balance < -1 and self._get_balance_factor(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
            
        return node
    
    def delete(self, value: Any) -> None:
        """
        Delete a value from the tree.
        
        Args:
            value: The value to delete
        """
        self.root = self._delete_recursive(self.root, value)
    
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
    
    def get_min(self) -> Any:
        """
        Find the minimum value in the tree.
        
        Returns:
            The minimum value
            
        Raises:
            ValueError: If the tree is empty
        """
        if not self.root:
            raise ValueError("Cannot find minimum in an empty tree")
            
        current = self.root
        while current.left:
            current = current.left
        return current.value
    
    def get_max(self) -> Any:
        """
        Find the maximum value in the tree.
        
        Returns:
            The maximum value
            
        Raises:
            ValueError: If the tree is empty
        """
        if not self.root:
            raise ValueError("Cannot find maximum in an empty tree")
            
        current = self.root
        while current.right:
            current = current.right
        return current.value
    
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
    
    def height(self) -> int:
        """
        Calculate the height of the tree.
        
        Returns:
            The height of the tree
        """
        if not self.root:
            return 0
        return self.root.height
    
    def is_balanced(self) -> bool:
        """
        Check if the tree is balanced.
        An AVL tree is always balanced by definition.
        
        Returns:
            True (always for a valid AVL tree)
        """
        return self._is_balanced_recursive(self.root)
    
    def _is_balanced_recursive(self, node: Optional[Node]) -> bool:
        """
        Recursively check if the subtree is balanced.
        
        Args:
            node: The root of the subtree
            
        Returns:
            True if the subtree is balanced, False otherwise
        """
        if node is None:
            return True
            
        balance = self._get_balance_factor(node)
        
        # Check if balance factor is within AVL bounds
        if abs(balance) > 1:
            return False
            
        # Recursively check left and right subtrees
        return (self._is_balanced_recursive(node.left) and 
                self._is_balanced_recursive(node.right))
    
    def clear(self) -> None:
        """
        Remove all elements from the tree.
        """
        self.root = None
        self.size = 0
    
    def is_empty(self) -> bool:
        """
        Check if the tree is empty.
        
        Returns:
            True if the tree is empty, False otherwise
        """
        return self.root is None
    
    def get_balance_factor(self, value: Any) -> Optional[int]:
        """
        Get the balance factor of the node with the given value.
        
        Args:
            value: The value of the node
            
        Returns:
            The balance factor, or None if the value is not found
        """
        node = self._find_node(value)
        if node is None:
            return None
        return self._get_balance_factor(node)
    
    def _find_node(self, value: Any) -> Optional[Node]:
        """
        Find the node with the given value.
        
        Args:
            value: The value to find
            
        Returns:
            The node with the value, or None if not found
        """
        current = self.root
        while current:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return None
    
    def validate(self) -> bool:
        """
        Validate that the tree satisfies all AVL tree properties.
        
        Returns:
            True if the tree is a valid AVL tree, False otherwise
        """
        return self._validate_recursive(self.root)
    
    def _validate_recursive(self, node: Optional[Node]) -> bool:
        """
        Recursively validate that the subtree satisfies all AVL tree properties.
        
        Args:
            node: The root of the subtree
            
        Returns:
            True if the subtree is a valid AVL tree, False otherwise
        """
        if node is None:
            return True
            
        # Check if the balance factor is within bounds
        balance = self._get_balance_factor(node)
        if abs(balance) > 1:
            return False
            
        # Check if the height is correctly calculated
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        if node.height != max(left_height, right_height) + 1:
            return False
            
        # Check if it's a valid BST
        if (node.left and node.left.value >= node.value) or \
           (node.right and node.right.value <= node.value):
            return False
            
        # Recursively check left and right subtrees
        return (self._validate_recursive(node.left) and 
                self._validate_recursive(node.right))


class TestAVLTree(unittest.TestCase):
    def setUp(self):
        self.tree = AVLTree()
        
    def test_init(self):
        self.assertIsNone(self.tree.root)
        self.assertEqual(len(self.tree), 0)
        self.assertTrue(self.tree.is_empty())
        
    def test_insert_search(self):
        # Insert values
        self.tree.insert(10)
        self.tree.insert(20)
        self.tree.insert(30)
        
        # Check size and search
        self.assertEqual(len(self.tree), 3)
        self.assertTrue(self.tree.search(10))
        self.assertTrue(self.tree.search(20))
        self.assertTrue(self.tree.search(30))
        self.assertFalse(self.tree.search(40))
        
        # Test __contains__
        self.assertTrue(10 in self.tree)
        self.assertFalse(40 in self.tree)
        
    def test_balance_after_insert(self):
        # Test right rotation (Left Left case)
        self.tree.insert(30)
        self.tree.insert(20)
        self.tree.insert(10)
        
        # After insertion and rotation, 20 should be the root
        self.assertEqual(self.tree.root.value, 20)
        self.assertEqual(self.tree.root.left.value, 10)
        self.assertEqual(self.tree.root.right.value, 30)
        
        # Check balance factor
        self.assertEqual(self._get_node_balance(self.tree.root), 0)  # Root
        self.assertEqual(self._get_node_balance(self.tree.root.left), 0)  # Left child
        self.assertEqual(self._get_node_balance(self.tree.root.right), 0)  # Right child
        
        # Test left rotation (Right Right case)
        self.tree.clear()
        self.tree.insert(10)
        self.tree.insert(20)
        self.tree.insert(30)
        
        # After insertion and rotation, 20 should be the root
        self.assertEqual(self.tree.root.value, 20)
        self.assertEqual(self.tree.root.left.value, 10)
        self.assertEqual(self.tree.root.right.value, 30)
        
        # Test Right Left case
        self.tree.clear()
        self.tree.insert(10)
        self.tree.insert(30)
        self.tree.insert(20)
        
        # After double rotation, 20 should be the root
        self.assertEqual(self.tree.root.value, 20)
        self.assertEqual(self.tree.root.left.value, 10)
        self.assertEqual(self.tree.root.right.value, 30)
        
        # Test Left Right case
        self.tree.clear()
        self.tree.insert(30)
        self.tree.insert(10)
        self.tree.insert(20)
        
        # After double rotation, 20 should be the root
        self.assertEqual(self.tree.root.value, 20)
        self.assertEqual(self.tree.root.left.value, 10)
        self.assertEqual(self.tree.root.right.value, 30)
        
    def test_delete(self):
        # Insert some values
        values = [9, 5, 10, 0, 6, 11, -1, 1, 2]
        for value in values:
            self.tree.insert(value)
            
        # Delete a leaf node
        self.tree.delete(-1)
        self.assertEqual(len(self.tree), 8)
        self.assertFalse(-1 in self.tree)
        
        # Delete a node with one child
        self.tree.delete(0)  # Has a right child
        self.assertEqual(len(self.tree), 7)
        self.assertFalse(0 in self.tree)
        self.assertTrue(1 in self.tree)
        
        # Delete a node with two children
        self.tree.delete(5)  # Has both left and right children
        self.assertEqual(len(self.tree), 6)
        self.assertFalse(5 in self.tree)
        self.assertTrue(6 in self.tree)
        
        # Check tree balance
        self.assertTrue(self.tree.validate())
        self.assertTrue(self.tree.is_balanced())
        
    def test_min_max(self):
        # Test with empty tree
        with self.assertRaises(ValueError):
            self.tree.get_min()
            
        with self.assertRaises(ValueError):
            self.tree.get_max()
            
        # Insert values
        values = [5, 3, 8, 1, 4, 7, 10]
        for value in values:
            self.tree.insert(value)
            
        # Check min and max
        self.assertEqual(self.tree.get_min(), 1)
        self.assertEqual(self.tree.get_max(), 10)
        
    def test_traversals(self):
        # Insert values
        values = [5, 3, 8, 1, 4, 7, 10]
        for value in values:
            self.tree.insert(value)
            
        # Inorder traversal (should be sorted)
        self.assertEqual(self.tree.inorder_traversal(), [1, 3, 4, 5, 7, 8, 10])
        
        # Preorder traversal (depends on tree structure after balancing)
        # The exact order will depend on the rotations performed
        # Just check that all values are present
        preorder = self.tree.preorder_traversal()
        self.assertEqual(sorted(preorder), [1, 3, 4, 5, 7, 8, 10])
        
        # Postorder traversal (depends on tree structure after balancing)
        # Just check that all values are present
        postorder = self.tree.postorder_traversal()
        self.assertEqual(sorted(postorder), [1, 3, 4, 5, 7, 8, 10])
        
    def test_height(self):
        # Empty tree
        self.assertEqual(self.tree.height(), 0)
        
        # Insert values
        self.tree.insert(5)
        self.assertEqual(self.tree.height(), 1)
        
        self.tree.insert(3)
        self.assertEqual(self.tree.height(), 2)
        
        self.tree.insert(8)
        self.assertEqual(self.tree.height(), 2)
        
        # Add more values
        self.tree.insert(1)
        self.tree.insert(4)
        self.tree.insert(7)
        self.tree.insert(10)
        
        # With 7 values, a balanced BST should have height 3
        self.assertEqual(self.tree.height(), 3)
        
    def test_validate(self):
        # Insert values
        values = [5, 3, 8, 1, 4, 7, 10]
        for value in values:
            self.tree.insert(value)
            
        # A properly inserted AVL tree should be valid
        self.assertTrue(self.tree.validate())
        
        # Break the tree structure by directly modifying nodes
        if self.tree.root and self.tree.root.left:
            # Artificially make the tree invalid by creating an imbalance
            self.tree.root.left.height = 5  # This breaks the height property
            self.assertFalse(self.tree.validate())
            
    def test_clear(self):
        # Insert values
        values = [5, 3, 8, 1, 4, 7, 10]
        for value in values:
            self.tree.insert(value)
            
        self.assertEqual(len(self.tree), 7)
        
        # Clear the tree
        self.tree.clear()
        self.assertEqual(len(self.tree), 0)
        self.assertTrue(self.tree.is_empty())
        self.assertIsNone(self.tree.root)
    
    def _get_node_balance(self, node):
        """Helper method for tests to get balance factor"""
        if node is None:
            return 0
        return self.tree._get_height(node.left) - self.tree._get_height(node.right)

if __name__ == '__main__':
    unittest.main()
