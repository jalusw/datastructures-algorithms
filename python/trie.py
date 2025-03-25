import unittest
from typing import Any, Dict, List, Optional

class TrieNode:
    """
    A node in a Trie (Prefix Tree).
    
    Attributes:
        value: The character stored in this node
        children: Dictionary mapping characters to child nodes
        is_end: Whether this node represents the end of a word
        count: Number of words that end at this node
    """
    def __init__(self, value: str = ""):
        self.value = value
        self.children: Dict[str, TrieNode] = {}
        self.is_end = False
        self.count = 0

class Trie:
    """
    Trie (Prefix Tree) is a tree-like data structure used to store a dynamic set of strings.
    It is particularly useful for prefix-based operations like autocomplete.
    
    Methods:
        - insert(word) add a word to the trie
        - search(word) check if a word exists in the trie
        - starts_with(prefix) check if any word starts with the given prefix
        - delete(word) remove a word from the trie
        - get_all_words() return all words in the trie
        - count_words() return the total number of words
    """
    def __init__(self):
        """
        Initialize an empty trie.
        """
        self.root = TrieNode()
        self._word_count = 0
        
    def __str__(self) -> str:
        """
        Return the string representation of the trie.
        """
        return f"Trie(words={self._word_count})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the trie.
        """
        return self.__str__()
        
    def __len__(self) -> int:
        """
        Return the number of words in the trie.
        """
        return self._word_count
        
    def insert(self, word: str) -> None:
        """
        Insert a word into the trie.
        
        Args:
            word: the word to insert
        """
        if not word:
            return
            
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode(char)
            current = current.children[char]
            
        if not current.is_end:
            current.is_end = True
            current.count += 1
            self._word_count += 1
            
    def search(self, word: str) -> bool:
        """
        Check if a word exists in the trie.
        
        Args:
            word: the word to search for
            
        Returns:
            True if the word exists, False otherwise
        """
        if not word:
            return False
            
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
            
        return current.is_end
        
    def starts_with(self, prefix: str) -> bool:
        """
        Check if any word in the trie starts with the given prefix.
        
        Args:
            prefix: the prefix to check
            
        Returns:
            True if any word starts with the prefix, False otherwise
        """
        if not prefix:
            return True
            
        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
            
        return True
        
    def delete(self, word: str) -> bool:
        """
        Delete a word from the trie.
        
        Args:
            word: the word to delete
            
        Returns:
            True if the word was deleted, False if it didn't exist
        """
        if not word:
            return False
            
        def _delete_recursive(node: TrieNode, word: str, depth: int) -> bool:
            if depth == len(word):
                if node.is_end:
                    node.is_end = False
                    node.count -= 1
                    return True
                return False
                
            char = word[depth]
            if char not in node.children:
                return False
                
            should_delete = _delete_recursive(node.children[char], word, depth + 1)
            
            if should_delete and not node.children[char].children and not node.children[char].is_end:
                del node.children[char]
                
            return should_delete
            
        if self.search(word):
            _delete_recursive(self.root, word, 0)
            self._word_count -= 1
            return True
        return False
        
    def get_all_words(self) -> List[str]:
        """
        Get all words stored in the trie.
        
        Returns:
            List of all words in the trie
        """
        words = []
        
        def _collect_words(node: TrieNode, current_word: str) -> None:
            if node.is_end:
                words.append(current_word)
                
            for char, child in node.children.items():
                _collect_words(child, current_word + char)
                
        _collect_words(self.root, "")
        return words
        
    def count_words(self) -> int:
        """
        Get the total number of words in the trie.
        
        Returns:
            The number of words
        """
        return self._word_count
        
    def clear(self) -> None:
        """
        Remove all words from the trie.
        """
        self.root = TrieNode()
        self._word_count = 0


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        
    def test_init(self):
        self.assertEqual(len(self.trie), 0)
        self.assertIsInstance(self.trie.root, TrieNode)
        
    def test_insert(self):
        self.trie.insert("hello")
        self.assertEqual(len(self.trie), 1)
        self.assertTrue(self.trie.search("hello"))
        
        self.trie.insert("world")
        self.assertEqual(len(self.trie), 2)
        self.assertTrue(self.trie.search("world"))
        
    def test_search(self):
        self.trie.insert("hello")
        self.trie.insert("world")
        
        self.assertTrue(self.trie.search("hello"))
        self.assertTrue(self.trie.search("world"))
        self.assertFalse(self.trie.search("hell"))
        self.assertFalse(self.trie.search("worl"))
        
    def test_starts_with(self):
        self.trie.insert("hello")
        self.trie.insert("world")
        
        self.assertTrue(self.trie.starts_with("he"))
        self.assertTrue(self.trie.starts_with("wo"))
        self.assertFalse(self.trie.starts_with("x"))
        self.assertFalse(self.trie.starts_with("heo"))
        
    def test_delete(self):
        self.trie.insert("hello")
        self.trie.insert("world")
        
        self.assertTrue(self.trie.delete("hello"))
        self.assertEqual(len(self.trie), 1)
        self.assertFalse(self.trie.search("hello"))
        self.assertTrue(self.trie.search("world"))
        
        self.assertFalse(self.trie.delete("nonexistent"))
        self.assertEqual(len(self.trie), 1)
        
    def test_get_all_words(self):
        words = ["hello", "world", "hi", "hey"]
        for word in words:
            self.trie.insert(word)
            
        all_words = self.trie.get_all_words()
        self.assertEqual(set(all_words), set(words))
        
    def test_duplicate_words(self):
        self.trie.insert("hello")
        self.trie.insert("hello")
        self.assertEqual(len(self.trie), 1)  # Should not count duplicates
        
        self.trie.delete("hello")
        self.assertEqual(len(self.trie), 0)
        
    def test_empty_string(self):
        self.trie.insert("")
        self.assertEqual(len(self.trie), 0)
        
        self.trie.insert("a")
        self.trie.insert("")
        self.assertEqual(len(self.trie), 1)
        
    def test_clear(self):
        self.trie.insert("hello")
        self.trie.insert("world")
        self.assertEqual(len(self.trie), 2)
        
        self.trie.clear()
        self.assertEqual(len(self.trie), 0)
        self.assertFalse(self.trie.search("hello"))
        self.assertFalse(self.trie.search("world"))
        
    def test_prefix_count(self):
        self.trie.insert("hello")
        self.trie.insert("help")
        self.trie.insert("helmet")
        
        self.assertTrue(self.trie.starts_with("hel"))
        self.assertTrue(self.trie.starts_with("help"))
        self.assertFalse(self.trie.starts_with("heo"))
        
    def test_complex_words(self):
        words = ["cat", "cats", "catch", "catching", "caught"]
        for word in words:
            self.trie.insert(word)
            
        self.assertEqual(len(self.trie), 5)
        self.assertTrue(self.trie.search("catch"))
        self.assertTrue(self.trie.starts_with("cat"))
        
        self.trie.delete("catch")
        self.assertEqual(len(self.trie), 4)
        self.assertFalse(self.trie.search("catch"))
        self.assertTrue(self.trie.starts_with("cat"))

if __name__ == '__main__':
    unittest.main() 