import unittest
from typing import Any, Optional, List
from binary_tree import Node, BinaryTree

class FullBinaryTree(BinaryTree):
    """
    FullBinaryTree is a binary tree where every node has 0 or 2 children.
    
    A full binary tree is a special type of binary tree where every internal
    node has exactly two children, and all leaf nodes are at the same level.
    
    Inherits all methods from BinaryTree and enforces the full property.
    """
    
    def insert_left(self, value: Any, parent_index: int = 0) -> bool:
        """
        Insert a left child at the specified parent index.
        
        For a full binary tree, we enforce that if a node has a left child,
        it must also have a right child, and vice versa.
        
        Args:
            value: The value to insert
            parent_index: The level-order index of the parent node
            
        Returns:
            True if successful, False otherwise
        """
        parent = self._find_node_by_index(parent_index)
        if not parent:
            return False
            
        # Cannot insert only a left child - must have both or none
        if parent.right is not None and parent.left is None:
            # Adding left child to complete the pair
            parent.left = Node(value)
            self.size += 1
            return True
            
        if parent.left is not None:
            # Already has a left child
            return False
            
        if parent.right is None:
            # Must add both children at once for a full binary tree
            # This insertion alone would leave the tree in an invalid state
            return False
            
        parent.left = Node(value)
        self.size += 1
        return True
        
    def insert_right(self, value: Any, parent_index: int = 0) -> bool:
        """
        Insert a right child at the specified parent index.
        
        For a full binary tree, we enforce that if a node has a right child,
        it must also have a left child, and vice versa.
        
        Args:
            value: The value to insert
            parent_index: The level-order index of the parent node
            
        Returns:
            True if successful, False otherwise
        """
        parent = self._find_node_by_index(parent_index)
        if not parent:
            return False
            
        # Cannot insert only a right child - must have both or none
        if parent.left is not None and parent.right is None:
            # Adding right child to complete the pair
            parent.right = Node(value)
            self.size += 1
            return True
            
        if parent.right is not None:
            # Already has a right child
            return False
            
        if parent.left is None:
            # Must add both children at once for a full binary tree
            # This insertion alone would leave the tree in an invalid state
            return False
            
        parent.right = Node(value)
        self.size += 1
        return True
    
    def insert_pair(self, left_value: Any, right_value: Any, parent_index: int = 0) -> bool:
        """
        Insert a pair of children (left and right) at the specified parent index.
        
        This is the preferred way to insert into a full binary tree.
        
        Args:
            left_value: The value for the left child
            right_value: The value for the right child
            parent_index: The level-order index of the parent node
            
        Returns:
            True if successful, False otherwise
        """
        parent = self._find_node_by_index(parent_index)
        if not parent:
            return False
            
        if parent.left is not None or parent.right is not None:
            # Already has at least one child
            return False
            
        parent.left = Node(left_value)
        parent.right = Node(right_value)
        self.size += 2
        return True
    
    def validate(self) -> bool:
        """
        Validate that the tree satisfies the full binary tree property.
        
        Returns:
            True if the tree is a valid full binary tree, False otherwise
        """
        return self.is_full()


class TestFullBinaryTree(unittest.TestCase):
    def setUp(self):
        self.tree = FullBinaryTree()
        
    def test_init(self):
        self.assertIsNone(self.tree.root)
        self.assertEqual(len(self.tree), 0)
        self.assertTrue(self.tree.is_empty())
        
        tree_with_root = FullBinaryTree(10)
        self.assertEqual(tree_with_root.root.value, 10)
        self.assertEqual(len(tree_with_root), 1)
        
    def test_insert_pair(self):
        self.tree.set_root(1)
        
        # Insert a pair of children to root
        self.assertTrue(self.tree.insert_pair(2, 3))
        self.assertEqual(len(self.tree), 3)
        self.assertEqual(self.tree.root.left.value, 2)
        self.assertEqual(self.tree.root.right.value, 3)
        
        # Insert children to the left child
        self.assertTrue(self.tree.insert_pair(4, 5, 1))  # Root's left child has index 1
        self.assertEqual(len(self.tree), 5)
        
        # Insert children to the right child
        self.assertTrue(self.tree.insert_pair(6, 7, 2))  # Root's right child has index 2
        self.assertEqual(len(self.tree), 7)
        
        # Try to insert to a node that already has children
        self.assertFalse(self.tree.insert_pair(8, 9, 1))
        self.assertEqual(len(self.tree), 7)
        
        # Try to insert to a non-existent node
        self.assertFalse(self.tree.insert_pair(10, 11, 100))
        self.assertEqual(len(self.tree), 7)
        
    def test_insert_left_right_restrictions(self):
        self.tree.set_root(1)
        
        # Cannot insert only left child
        self.assertFalse(self.tree.insert_left(2))
        self.assertEqual(len(self.tree), 1)
        
        # Cannot insert only right child
        self.assertFalse(self.tree.insert_right(3))
        self.assertEqual(len(self.tree), 1)
        
        # Insert a pair first
        self.tree.insert_pair(2, 3)
        
        # Now cannot insert left or right individually
        self.assertFalse(self.tree.insert_left(4, 1))
        self.assertFalse(self.tree.insert_right(5, 2))
        
        # Insert another pair
        self.tree.insert_pair(4, 5, 1)
        
        # Validate the tree is still full
        self.assertTrue(self.tree.is_full())
        self.assertTrue(self.tree.validate())
        
    def test_traversals(self):
        self.tree.set_root(1)
        self.tree.insert_pair(2, 3)
        self.tree.insert_pair(4, 5, 1)
        self.tree.insert_pair(6, 7, 2)
        
        # Level order traversal
        self.assertEqual(self.tree.level_order_traversal(), [1, 2, 3, 4, 5, 6, 7])
        
        # Inorder traversal: left, root, right
        self.assertEqual(self.tree.inorder_traversal(), [4, 2, 5, 1, 6, 3, 7])
        
        # Preorder traversal: root, left, right
        self.assertEqual(self.tree.preorder_traversal(), [1, 2, 4, 5, 3, 6, 7])
        
        # Postorder traversal: left, right, root
        self.assertEqual(self.tree.postorder_traversal(), [4, 5, 2, 6, 7, 3, 1])
        
    def test_height_and_properties(self):
        # Empty tree
        self.assertEqual(self.tree.height(), 0)
        self.assertTrue(self.tree.is_full())
        self.assertTrue(self.tree.is_perfect()) # Empty tree is perfect
        
        # Single node
        self.tree.set_root(1)
        self.assertEqual(self.tree.height(), 1)
        self.assertTrue(self.tree.is_full())
        self.assertTrue(self.tree.is_perfect())
        
        # Full binary tree with height 2
        self.tree.insert_pair(2, 3)
        self.assertEqual(self.tree.height(), 2)
        self.assertTrue(self.tree.is_full())
        self.assertTrue(self.tree.is_perfect())
        
        # Full binary tree with height 3
        self.tree.insert_pair(4, 5, 1)
        self.tree.insert_pair(6, 7, 2)
        self.assertEqual(self.tree.height(), 3)
        self.assertTrue(self.tree.is_full())
        self.assertTrue(self.tree.is_perfect())
        
    def test_is_balanced(self):
        # Full trees are always balanced
        self.tree.set_root(1)
        self.tree.insert_pair(2, 3)
        self.assertTrue(self.tree.is_balanced())
        
        self.tree.insert_pair(4, 5, 1)
        self.tree.insert_pair(6, 7, 2)
        self.assertTrue(self.tree.is_balanced())
        
    def test_is_complete(self):
        # Full trees are always complete
        self.tree.set_root(1)
        self.tree.insert_pair(2, 3)
        self.assertTrue(self.tree.is_complete())
        
        self.tree.insert_pair(4, 5, 1)
        self.tree.insert_pair(6, 7, 2)
        self.assertTrue(self.tree.is_complete())
        
    def test_clear(self):
        self.tree.set_root(1)
        self.tree.insert_pair(2, 3)
        self.assertEqual(len(self.tree), 3)
        
        self.tree.clear()
        self.assertEqual(len(self.tree), 0)
        self.assertTrue(self.tree.is_empty())
        self.assertIsNone(self.tree.root)
        
    def test_validate(self):
        self.tree.set_root(1)
        self.tree.insert_pair(2, 3)
        self.assertTrue(self.tree.validate())
        
        # Create a non-full tree by directly modifying nodes
        # (breaking the full property)
        self.tree.root.left.left = Node(4)  # Add only left child, not right
        self.size = 4  # Manually update size
        
        # The tree should no longer validate as full
        self.assertFalse(self.tree.validate())

if __name__ == '__main__':
    unittest.main()
