import unittest
from typing import Any, Optional, List, Callable

class Node:
    """
    A node in a binary tree.
    
    Attributes:
        value: The value stored in the node
        left: Reference to the left child node
        right: Reference to the right child node
    """
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    """
    BinaryTree is a tree data structure where each node has at most two children.
    Unlike a binary search tree, there is no ordering constraint.
    
    Methods:
        - insert_left(value, parent_index): Insert a left child at the specified parent
        - insert_right(value, parent_index): Insert a right child at the specified parent
        - level_order_traversal(): Return values in level order
        - inorder_traversal(): Return values in inorder
        - preorder_traversal(): Return values in preorder
        - postorder_traversal(): Return values in postorder
        - height(): Return the height of the tree
        - is_balanced(): Check if the tree is balanced
    """
    def __init__(self, root_value=None):
        """
        Initialize a binary tree, optionally with a root value.
        
        Args:
            root_value: Optional value for the root node
        """
        self.root = Node(root_value) if root_value is not None else None
        self.size = 1 if root_value is not None else 0
        
    def __str__(self) -> str:
        """
        Return the string representation of the tree.
        """
        if not self.root:
            return "[]"
        
        values = self.level_order_traversal()
        return f"{values}"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the tree.
        """
        return f"BinaryTree({self.__str__()})"
        
    def __len__(self) -> int:
        """
        Return the number of nodes in the tree.
        """
        return self.size
    
    def _find_node_by_index(self, index: int) -> Optional[Node]:
        """
        Find a node by its level-order index.
        
        Args:
            index: The level-order index of the node (0 is root)
            
        Returns:
            The node at the specified index or None if not found
        """
        if not self.root or index < 0:
            return None
            
        # Use breadth-first search to find the node
        queue = [self.root]
        current_index = 0
        
        while queue and current_index <= index:
            node = queue.pop(0)
            
            if current_index == index:
                return node
                
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
            current_index += 1
            
        return None
        
    def insert_left(self, value: Any, parent_index: int = 0) -> bool:
        """
        Insert a left child at the specified parent index.
        
        Args:
            value: The value to insert
            parent_index: The level-order index of the parent node
            
        Returns:
            True if successful, False otherwise
        """
        parent = self._find_node_by_index(parent_index)
        if not parent:
            return False
            
        if parent.left:  # Left child already exists
            return False
            
        parent.left = Node(value)
        self.size += 1
        return True
        
    def insert_right(self, value: Any, parent_index: int = 0) -> bool:
        """
        Insert a right child at the specified parent index.
        
        Args:
            value: The value to insert
            parent_index: The level-order index of the parent node
            
        Returns:
            True if successful, False otherwise
        """
        parent = self._find_node_by_index(parent_index)
        if not parent:
            return False
            
        if parent.right:  # Right child already exists
            return False
            
        parent.right = Node(value)
        self.size += 1
        return True
    
    def set_root(self, value: Any) -> None:
        """
        Set or change the root node value.
        
        Args:
            value: The value to set
        """
        if not self.root:
            self.root = Node(value)
            self.size = 1
        else:
            self.root.value = value
    
    def level_order_traversal(self) -> List[Any]:
        """
        Traverse the tree in level order (breadth-first).
        
        Returns:
            List of values in level order traversal
        """
        if not self.root:
            return []
            
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        return result
    
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
    
    def _height_recursive(self, node: Optional[Node]) -> int:
        """
        Recursively calculate the height of the subtree.
        
        Args:
            node: The root of the subtree
            
        Returns:
            The height of the subtree
        """
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))
        
    def height(self) -> int:
        """
        Calculate the height of the tree.
        
        Returns:
            The height of the tree
        """
        return self._height_recursive(self.root)
    
    def _is_balanced_recursive(self, node: Optional[Node]) -> bool:
        """
        Recursively check if the subtree is balanced.
        A balanced tree has the height difference between left and right subtrees
        of any node not exceeding 1.
        
        Args:
            node: The root of the subtree
            
        Returns:
            True if the subtree is balanced, False otherwise
        """
        if node is None:
            return True
            
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        if abs(left_height - right_height) > 1:
            return False
            
        return (self._is_balanced_recursive(node.left) and 
                self._is_balanced_recursive(node.right))
    
    def is_balanced(self) -> bool:
        """
        Check if the tree is balanced.
        
        Returns:
            True if the tree is balanced, False otherwise
        """
        return self._is_balanced_recursive(self.root)
    
    def _is_full_recursive(self, node: Optional[Node]) -> bool:
        """
        Recursively check if the subtree is full.
        A full tree has every node with either 0 or 2 children.
        
        Args:
            node: The root of the subtree
            
        Returns:
            True if the subtree is full, False otherwise
        """
        if node is None:
            return True
            
        # Leaf node
        if node.left is None and node.right is None:
            return True
            
        # Node with exactly two children
        if node.left is not None and node.right is not None:
            return (self._is_full_recursive(node.left) and 
                    self._is_full_recursive(node.right))
                    
        # Node with only one child
        return False
    
    def is_full(self) -> bool:
        """
        Check if the tree is a full binary tree.
        A full binary tree has every node with either 0 or 2 children.
        
        Returns:
            True if the tree is full, False otherwise
        """
        return self._is_full_recursive(self.root)
    
    def _is_perfect_recursive(self, node: Optional[Node], depth: int, level: int = 0) -> bool:
        """
        Recursively check if the subtree is perfect.
        
        Args:
            node: The root of the subtree
            depth: The depth of the tree
            level: The current level
            
        Returns:
            True if the subtree is perfect, False otherwise
        """
        if node is None:
            return True
            
        # If leaf node, check its level against depth
        if node.left is None and node.right is None:
            return level == depth
            
        # If internal node, check if it has both children
        if node.left is None or node.right is None:
            return False
            
        # Recursively check left and right subtrees
        return (self._is_perfect_recursive(node.left, depth, level + 1) and
                self._is_perfect_recursive(node.right, depth, level + 1))
    
    def is_perfect(self) -> bool:
        """
        Check if the tree is a perfect binary tree.
        A perfect binary tree has all internal nodes having exactly two children
        and all leaves at the same level.
        
        Returns:
            True if the tree is perfect, False otherwise
        """
        if not self.root:
            return True
            
        depth = 0
        node = self.root
        # Calculate the leftmost depth
        while node.left:
            depth += 1
            node = node.left
            
        return self._is_perfect_recursive(self.root, depth)
    
    def is_complete(self) -> bool:
        """
        Check if the tree is a complete binary tree.
        A complete binary tree is a binary tree where every level, 
        except possibly the last, is completely filled, and all nodes 
        in the last level are as far left as possible.
        
        Returns:
            True if the tree is complete, False otherwise
        """
        if not self.root:
            return True
            
        queue = [self.root]
        flag = False  # Flag to mark the occurrence of a non-full node
        
        while queue:
            node = queue.pop(0)
            
            # If we've seen a non-full node before and this node has children
            if flag and (node.left or node.right):
                return False
                
            if node.left is None and node.right:
                return False  # Violation: right child without left child
                
            if node.left:
                queue.append(node.left)
            else:
                flag = True  # If left child is None, mark flag
                
            if node.right:
                queue.append(node.right)
            else:
                flag = True  # If right child is None, mark flag
                
        return True
    
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


class TestBinaryTree(unittest.TestCase):
    def setUp(self):
        self.tree = BinaryTree()
        
    def test_init(self):
        self.assertIsNone(self.tree.root)
        self.assertEqual(len(self.tree), 0)
        self.assertTrue(self.tree.is_empty())
        
        tree_with_root = BinaryTree(10)
        self.assertEqual(tree_with_root.root.value, 10)
        self.assertEqual(len(tree_with_root), 1)
        
    def test_set_root(self):
        self.tree.set_root(5)
        self.assertEqual(self.tree.root.value, 5)
        self.assertEqual(len(self.tree), 1)
        
        self.tree.set_root(10)
        self.assertEqual(self.tree.root.value, 10)
        self.assertEqual(len(self.tree), 1)  # Size doesn't change when updating
        
    def test_insert_left_right(self):
        self.tree.set_root(1)
        
        # Insert left and right children to root
        self.assertTrue(self.tree.insert_left(2))
        self.assertTrue(self.tree.insert_right(3))
        self.assertEqual(len(self.tree), 3)
        self.assertEqual(self.tree.root.left.value, 2)
        self.assertEqual(self.tree.root.right.value, 3)
        
        # Insert children to the left child
        self.assertTrue(self.tree.insert_left(4, 1))  # Root's left child has index 1
        self.assertTrue(self.tree.insert_right(5, 1))
        self.assertEqual(len(self.tree), 5)
        
        # Insert children to the right child
        self.assertTrue(self.tree.insert_left(6, 2))  # Root's right child has index 2
        self.assertTrue(self.tree.insert_right(7, 2))
        self.assertEqual(len(self.tree), 7)
        
        # Try to insert left to a node that already has left child
        self.assertFalse(self.tree.insert_left(8, 1))
        self.assertEqual(len(self.tree), 7)
        
        # Try to insert to a non-existent node
        self.assertFalse(self.tree.insert_left(9, 100))
        self.assertEqual(len(self.tree), 7)
        
    def test_traversals(self):
        self.tree.set_root(1)
        self.tree.insert_left(2)
        self.tree.insert_right(3)
        self.tree.insert_left(4, 1)
        self.tree.insert_right(5, 1)
        self.tree.insert_left(6, 2)
        self.tree.insert_right(7, 2)
        
        # Level order traversal
        self.assertEqual(self.tree.level_order_traversal(), [1, 2, 3, 4, 5, 6, 7])
        
        # Inorder traversal: left, root, right
        self.assertEqual(self.tree.inorder_traversal(), [4, 2, 5, 1, 6, 3, 7])
        
        # Preorder traversal: root, left, right
        self.assertEqual(self.tree.preorder_traversal(), [1, 2, 4, 5, 3, 6, 7])
        
        # Postorder traversal: left, right, root
        self.assertEqual(self.tree.postorder_traversal(), [4, 5, 2, 6, 7, 3, 1])
        
    def test_height(self):
        self.assertEqual(self.tree.height(), 0)  # Empty tree
        
        self.tree.set_root(1)
        self.assertEqual(self.tree.height(), 1)  # Just root
        
        self.tree.insert_left(2)
        self.assertEqual(self.tree.height(), 2)  # Root and one child
        
        self.tree.insert_right(3)
        self.assertEqual(self.tree.height(), 2)  # Balanced with left and right
        
        self.tree.insert_left(4, 1)  # Add to the left subtree
        self.assertEqual(self.tree.height(), 3)
        
    def test_is_balanced(self):
        # Empty tree is balanced
        self.assertTrue(self.tree.is_balanced())
        
        # Single node is balanced
        self.tree.set_root(1)
        self.assertTrue(self.tree.is_balanced())
        
        # Balanced tree with height 2
        self.tree.insert_left(2)
        self.tree.insert_right(3)
        self.assertTrue(self.tree.is_balanced())
        
        # Unbalanced tree
        self.tree.insert_left(4, 1)
        self.tree.insert_left(5, 3)  # This makes the right subtree deeper
        self.assertFalse(self.tree.is_balanced())
        
    def test_is_full(self):
        # Empty tree is full
        self.assertTrue(self.tree.is_full())
        
        # Single node is full
        self.tree.set_root(1)
        self.assertTrue(self.tree.is_full())
        
        # Node with one child is not full
        self.tree.insert_left(2)
        self.assertFalse(self.tree.is_full())
        
        # Node with two children is full
        self.tree.insert_right(3)
        self.assertTrue(self.tree.is_full())
        
        # Full binary tree
        self.tree.insert_left(4, 1)
        self.tree.insert_right(5, 1)
        self.assertTrue(self.tree.is_full())
        
        # Not a full binary tree (node with only one child)
        self.tree.insert_left(6, 2)
        self.assertFalse(self.tree.is_full())
        
    def test_is_perfect(self):
        # Empty tree is perfect
        self.assertTrue(self.tree.is_perfect())
        
        # Single node is perfect
        self.tree.set_root(1)
        self.assertTrue(self.tree.is_perfect())
        
        # Not perfect (one node lacks a child)
        self.tree.insert_left(2)
        self.assertFalse(self.tree.is_perfect())
        
        # Perfect tree of height 2
        self.tree.insert_right(3)
        self.assertTrue(self.tree.is_perfect())
        
        # Not perfect (height 3 but not all leaves at same level)
        self.tree.insert_left(4, 1)
        self.assertFalse(self.tree.is_perfect())
        
        # Perfect tree of height 3
        self.tree.insert_right(5, 1)
        self.tree.insert_left(6, 2)
        self.tree.insert_right(7, 2)
        self.assertTrue(self.tree.is_perfect())
        
    def test_is_complete(self):
        # Empty tree is complete
        self.assertTrue(self.tree.is_complete())
        
        # Single node is complete
        self.tree.set_root(1)
        self.assertTrue(self.tree.is_complete())
        
        # Complete tree
        self.tree.insert_left(2)
        self.assertTrue(self.tree.is_complete())
        
        self.tree.insert_right(3)
        self.assertTrue(self.tree.is_complete())
        
        self.tree.insert_left(4, 1)
        self.assertTrue(self.tree.is_complete())
        
        self.tree.insert_right(5, 1)
        self.assertTrue(self.tree.is_complete())
        
        self.tree.insert_left(6, 2)
        self.assertTrue(self.tree.is_complete())
        
        # Still complete
        self.tree.insert_right(7, 2)
        self.assertTrue(self.tree.is_complete())
        
        # No longer complete (gap in last level)
        tree2 = BinaryTree(1)
        tree2.insert_left(2)
        tree2.insert_right(3)
        tree2.insert_right(4, 1)  # Skip left child of node at index 1
        self.assertFalse(tree2.is_complete())
        
        # No longer complete (right without left)
        tree3 = BinaryTree(1)
        tree3.insert_right(2)  # Only right child
        self.assertFalse(tree3.is_complete())
        
    def test_clear(self):
        self.tree.set_root(1)
        self.tree.insert_left(2)
        self.tree.insert_right(3)
        self.assertEqual(len(self.tree), 3)
        
        self.tree.clear()
        self.assertEqual(len(self.tree), 0)
        self.assertTrue(self.tree.is_empty())
        self.assertIsNone(self.tree.root)

if __name__ == '__main__':
    unittest.main()
