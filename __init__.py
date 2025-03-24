"""
Data Structures and Algorithms (DSA) Package

This package contains implementations of various data structures and algorithms.
"""

# Basic data structures
from .array import Array
from .singly_linked_list import SinglyLinkedList, Node as SLLNode
from .doubly_linked_list import DoublyLinkedList, Node as DLLNode
from .circular_linked_list import CircularLinkedList, Node as CLLNode
from .circular_doubly_linked_list import CircularDoublyLinkedList, Node as CDLLNode
from .binary_search_tree import BinarySearchTree, Node as BSTNode
from .binary_tree import BinaryTree, Node as BTNode
from .full_binary_tree import FullBinaryTree
from .avl_tree import AVLTree, Node as AVLNode
from .red_black_tree import RedBlackTree, Node as RBNode
from .b_tree import BTree, Node as BTNode
from .trie import Trie, TrieNode
from .hash_table import HashTable, HashNode

# Queue-like data structures
from .queue import Queue
from .deque import Deque
from .priority_queue import PriorityQueue
from .monotonic_queue import MonotonicQueue

# Stack-like data structures
from .stack import Stack
from .monotonic_stack import MonotonicStack

# Heap data structures
from .min_heap import MinHeap
from .max_heap import MaxHeap

# Advanced data structures
from .bloom_filter import BloomFilter
from .sparse_table import SparseTable

__all__ = [
    # Basic data structures
    'Array',
    'SinglyLinkedList', 'SLLNode',
    'DoublyLinkedList', 'DLLNode',
    'CircularLinkedList', 'CLLNode',
    'CircularDoublyLinkedList', 'CDLLNode',
    'BinarySearchTree', 'BSTNode',
    'BinaryTree', 'BTNode',
    'FullBinaryTree',
    'AVLTree', 'AVLNode',
    'RedBlackTree', 'RBNode',
    'BTree', 'BTNode',
    'Trie', 'TrieNode',
    'HashTable', 'HashNode',
    
    # Queue-like data structures
    'Queue',
    'Deque',
    'PriorityQueue',
    'MonotonicQueue',
    
    # Stack-like data structures
    'Stack',
    'MonotonicStack',
    
    # Heap data structures
    'MinHeap',
    'MaxHeap',
    
    # Advanced data structures
    'BloomFilter',
    'SparseTable'
]

__version__ = '0.1.0'
