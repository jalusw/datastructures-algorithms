from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

class SuffixTreeNode:
    """Node in a suffix tree."""
    def __init__(self, start: int, end: int, parent: Optional['SuffixTreeNode'] = None):
        self.start = start
        self.end = end
        self.parent = parent
        self.children: Dict[str, SuffixTreeNode] = {}
        self.suffix_link: Optional[SuffixTreeNode] = None
        self.leaf_count = 0

class SuffixTree:
    """
    A suffix tree is a compressed trie containing all the suffixes of a given text.
    It provides O(m) pattern matching time complexity, where m is the pattern length.
    
    Properties:
        - O(n) space complexity
        - O(m) pattern matching
        - O(n) construction time
        - Supports multiple pattern matching
        - Efficient for string operations
    """
    
    def __init__(self, text: str):
        """
        Initialize a suffix tree with the given text.
        
        Args:
            text: The text to build the suffix tree from
        """
        self.text = text + '$'  # Add terminal character
        self.root = SuffixTreeNode(-1, -1)
        self._build_tree()
    
    def _build_tree(self) -> None:
        """Build the suffix tree using Ukkonen's algorithm."""
        n = len(self.text)
        active_node = self.root
        active_edge = -1
        active_length = 0
        
        for i in range(n):
            current_char = self.text[i]
            previous_node = None
            
            while True:
                if active_length == 0:
                    active_edge = i
                
                if current_char not in active_node.children:
                    # Create new leaf node
                    leaf = SuffixTreeNode(i, n - 1, active_node)
                    active_node.children[current_char] = leaf
                    leaf.leaf_count = 1
                    
                    if previous_node is not None:
                        previous_node.suffix_link = active_node
                        previous_node = None
                    
                    if active_node == self.root:
                        active_length = max(0, active_length - 1)
                        active_edge = i - active_length
                    else:
                        active_node = active_node.suffix_link or self.root
                        active_length = max(0, active_length - 1)
                        active_edge = i - active_length
                    continue
                
                next_node = active_node.children[current_char]
                edge_length = next_node.end - next_node.start + 1
                
                if active_length >= edge_length:
                    active_length -= edge_length
                    active_edge += edge_length
                    active_node = next_node
                    continue
                
                if self.text[next_node.start + active_length] == current_char:
                    active_length += 1
                    if previous_node is not None:
                        previous_node.suffix_link = active_node
                        previous_node = None
                    break
                
                # Split edge
                split_node = SuffixTreeNode(next_node.start, next_node.start + active_length - 1, active_node)
                leaf = SuffixTreeNode(i, n - 1, split_node)
                next_node.start += active_length
                next_node.parent = split_node
                
                split_node.children[current_char] = leaf
                split_node.children[self.text[next_node.start]] = next_node
                split_node.leaf_count = next_node.leaf_count + 1
                
                active_node.children[self.text[split_node.start]] = split_node
                
                if previous_node is not None:
                    previous_node.suffix_link = split_node
                    previous_node = None
                
                previous_node = split_node
                
                if active_node == self.root:
                    active_length = max(0, active_length - 1)
                    active_edge = i - active_length
                else:
                    active_node = active_node.suffix_link or self.root
                    active_length = max(0, active_length - 1)
                    active_edge = i - active_length
    
    def search(self, pattern: str) -> List[int]:
        """
        Search for a pattern in the text.
        
        Args:
            pattern: The pattern to search for
            
        Returns:
            List of starting positions where the pattern occurs
        """
        if not pattern:
            return []
        
        current = self.root
        pattern_length = len(pattern)
        current_length = 0
        
        while current_length < pattern_length:
            current_char = pattern[current_length]
            if current_char not in current.children:
                return []
            
            child = current.children[current_char]
            edge_length = child.end - child.start + 1
            
            # Compare characters along the edge
            for i in range(min(edge_length, pattern_length - current_length)):
                if self.text[child.start + i] != pattern[current_length + i]:
                    return []
            
            current_length += edge_length
            if current_length < pattern_length:
                current = child
        
        # Collect all leaf positions
        positions = []
        self._collect_positions(child, positions)
        return positions
    
    def _collect_positions(self, node: SuffixTreeNode, positions: List[int]) -> None:
        """Collect all leaf positions under a node."""
        if not node.children:
            positions.append(node.start)
            return
        
        for child in node.children.values():
            self._collect_positions(child, positions)
    
    def get_substring_count(self) -> int:
        """
        Get the number of distinct substrings in the text.
        
        Returns:
            Number of distinct substrings
        """
        return self._count_substrings(self.root)
    
    def _count_substrings(self, node: SuffixTreeNode) -> int:
        """Count distinct substrings under a node."""
        count = 0
        for child in node.children.values():
            count += child.end - child.start + 1
            count += self._count_substrings(child)
        return count
    
    def get_longest_repeated_substring(self) -> str:
        """
        Find the longest repeated substring in the text.
        
        Returns:
            The longest repeated substring
        """
        result = self._find_longest_repeated(self.root)
        if result:
            start, length = result
            return self.text[start:start + length]
        return ""
    
    def _find_longest_repeated(self, node: SuffixTreeNode) -> Optional[Tuple[int, int]]:
        """Find the longest repeated substring under a node."""
        if not node.children:
            return None
        
        max_length = 0
        max_start = -1
        
        for child in node.children.values():
            if child.leaf_count > 1:  # Node has multiple occurrences
                current_length = child.end - child.start + 1
                if current_length > max_length:
                    max_length = current_length
                    max_start = child.start
        
        for child in node.children.values():
            result = self._find_longest_repeated(child)
            if result:
                start, length = result
                if length > max_length:
                    max_length = length
                    max_start = start
        
        return (max_start, max_length) if max_length > 0 else None
    
    def clear(self) -> None:
        """Clear the suffix tree."""
        self.root = SuffixTreeNode(-1, -1) 