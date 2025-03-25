from typing import Optional, Tuple, List
import math

class RopeNode:
    """Node in a rope data structure."""
    def __init__(self, text: str = "", weight: int = 0):
        self.text = text
        self.weight = weight
        self.left: Optional[RopeNode] = None
        self.right: Optional[RopeNode] = None
        self.parent: Optional[RopeNode] = None
        self.height = 0
        self.size = len(text)

class Rope:
    """
    A rope data structure for efficient text editing operations.
    It provides O(log n) time complexity for split and concatenate operations.
    
    Properties:
        - O(log n) split and concatenate
        - O(log n) insert and delete
        - O(log n) substring operations
        - Efficient for large texts
        - Memory efficient
    """
    
    def __init__(self, text: str = ""):
        """
        Initialize a rope with the given text.
        
        Args:
            text: The initial text
        """
        self.root = RopeNode(text, len(text))
    
    def _update_metadata(self, node: RopeNode) -> None:
        """Update node metadata (weight, size, height)."""
        if node is None:
            return
        
        # Update weight
        node.weight = len(node.text) + (node.left.weight if node.left else 0)
        
        # Update size
        node.size = len(node.text) + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)
        
        # Update height
        node.height = 1 + max(
            node.left.height if node.left else 0,
            node.right.height if node.right else 0
        )
    
    def _balance(self, node: RopeNode) -> RopeNode:
        """Balance the rope at the given node."""
        if node is None:
            return None
        
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        
        if abs(left_height - right_height) <= 1:
            return node
        
        if left_height > right_height:
            # Left heavy
            if node.left.right and (node.left.left is None or node.left.left.height < node.left.right.height):
                # Left-Right case
                node.left = self._rotate_left(node.left)
            # Left-Left case
            return self._rotate_right(node)
        else:
            # Right heavy
            if node.right.left and (node.right.right is None or node.right.right.height < node.right.left.height):
                # Right-Left case
                node.right = self._rotate_right(node.right)
            # Right-Right case
            return self._rotate_left(node)
    
    def _rotate_left(self, node: RopeNode) -> RopeNode:
        """Perform a left rotation."""
        right = node.right
        right.parent = node.parent
        node.right = right.left
        if node.right:
            node.right.parent = node
        right.left = node
        node.parent = right
        self._update_metadata(node)
        self._update_metadata(right)
        return right
    
    def _rotate_right(self, node: RopeNode) -> RopeNode:
        """Perform a right rotation."""
        left = node.left
        left.parent = node.parent
        node.left = left.right
        if node.left:
            node.left.parent = node
        left.right = node
        node.parent = left
        self._update_metadata(node)
        self._update_metadata(left)
        return left
    
    def _find_node_at(self, index: int) -> Tuple[RopeNode, int]:
        """
        Find the node containing the character at the given index.
        
        Returns:
            Tuple of (node, local_index)
        """
        if index < 0 or index >= self.root.size:
            raise IndexError("Index out of range")
        
        current = self.root
        while current:
            left_size = current.left.size if current.left else 0
            if index < left_size:
                current = current.left
            else:
                index -= left_size
                if index < len(current.text):
                    return current, index
                index -= len(current.text)
                current = current.right
        
        raise IndexError("Index out of range")
    
    def _split_at(self, index: int) -> Tuple[RopeNode, RopeNode]:
        """
        Split the rope at the given index.
        
        Returns:
            Tuple of (left_rope, right_rope)
        """
        if index == 0:
            return None, self.root
        if index >= self.root.size:
            return self.root, None
        
        node, local_index = self._find_node_at(index)
        
        # Split the text in the node
        left_text = node.text[:local_index]
        right_text = node.text[local_index:]
        
        # Create new nodes
        left_node = RopeNode(left_text, len(left_text))
        right_node = RopeNode(right_text, len(right_text))
        
        # Update the tree structure
        if node.parent:
            if node == node.parent.left:
                node.parent.left = left_node
            else:
                node.parent.right = left_node
            left_node.parent = node.parent
        
        # Build the right subtree
        right_node.left = node.right
        if node.right:
            node.right.parent = right_node
        right_node.parent = node.parent
        
        # Update metadata
        self._update_metadata(left_node)
        self._update_metadata(right_node)
        
        return left_node, right_node
    
    def insert(self, index: int, text: str) -> None:
        """
        Insert text at the given index.
        
        Args:
            index: The position to insert at
            text: The text to insert
        """
        if not text:
            return
        
        left, right = self._split_at(index)
        new_node = RopeNode(text, len(text))
        
        if left is None:
            self.root = new_node
            new_node.right = right
            if right:
                right.parent = new_node
        else:
            self.root = left
            current = left
            while current.right:
                current = current.right
            current.right = new_node
            new_node.parent = current
            if right:
                new_node.right = right
                right.parent = new_node
        
        self._update_metadata(self.root)
    
    def delete(self, start: int, end: int) -> None:
        """
        Delete text from start to end.
        
        Args:
            start: Starting index
            end: Ending index
        """
        if start >= end or start < 0 or end > self.root.size:
            return
        
        left, right = self._split_at(start)
        _, right = self._split_at(end - start)
        
        if left is None:
            self.root = right
        else:
            self.root = left
            current = left
            while current.right:
                current = current.right
            current.right = right
            if right:
                right.parent = current
        
        self._update_metadata(self.root)
    
    def substring(self, start: int, end: int) -> str:
        """
        Get the substring from start to end.
        
        Args:
            start: Starting index
            end: Ending index
            
        Returns:
            The substring
        """
        if start >= end or start < 0 or end > self.root.size:
            return ""
        
        result = []
        self._collect_substring(self.root, start, end, result)
        return "".join(result)
    
    def _collect_substring(self, node: RopeNode, start: int, end: int, result: List[str]) -> None:
        """Collect characters for substring operation."""
        if node is None:
            return
        
        left_size = node.left.size if node.left else 0
        if start < left_size:
            self._collect_substring(node.left, start, min(end, left_size), result)
        
        if start < left_size + len(node.text) and end > left_size:
            text_start = max(0, start - left_size)
            text_end = min(len(node.text), end - left_size)
            result.append(node.text[text_start:text_end])
        
        if end > left_size + len(node.text):
            self._collect_substring(node.right, max(0, start - left_size - len(node.text)),
                                 end - left_size - len(node.text), result)
    
    def __len__(self) -> int:
        """Return the length of the rope."""
        return self.root.size
    
    def __str__(self) -> str:
        """Convert the rope to a string."""
        result = []
        self._collect_string(self.root, result)
        return "".join(result)
    
    def _collect_string(self, node: RopeNode, result: List[str]) -> None:
        """Collect all text in the rope."""
        if node is None:
            return
        self._collect_string(node.left, result)
        result.append(node.text)
        self._collect_string(node.right, result)
    
    def clear(self) -> None:
        """Clear the rope."""
        self.root = RopeNode() 