# Data Structures and Algorithms (DSA)

A comprehensive collection of data structures and algorithms implemented in Python. This library provides efficient, well-tested implementations that can be used for learning, interview preparation, and practical applications.

## Contents

### Basic Data Structures
- **Array**: A wrapper around Python's list with additional functionality
- **Linked Lists**: 
  - Singly Linked List
  - Doubly Linked List
  - Circular Linked List
  - Circular Doubly Linked List

### Tree Structures
- **Binary Tree**: A generic binary tree implementation with various property checks
- **Full Binary Tree**: A binary tree where each node has 0 or 2 children
- **Binary Search Tree**: Ordered binary tree with fast lookup/insert/delete
- **AVL Tree**: Self-balancing binary search tree

### Queue Structures
- **Queue**: First-In-First-Out (FIFO) data structure
- **Deque**: Double-ended queue supporting operations at both ends
- **Priority Queue**: Queue where elements have associated priorities
- **Monotonic Queue**: Queue that maintains elements in monotonic order

### Stack Structures
- **Stack**: Last-In-First-Out (LIFO) data structure
- **Monotonic Stack**: Stack that maintains elements in monotonic order

### Heap Structures
- **Min Heap**: Binary heap where parent is smaller than its children
- **Max Heap**: Binary heap where parent is larger than its children

### Advanced Data Structures
- **Bloom Filter**: Space-efficient probabilistic data structure for membership testing
- **Sparse Table**: Data structure for efficient range queries

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/dsa.git
cd dsa
```

## Usage

Import and use any of the data structures:

```python
from dsa import SinglyLinkedList, Stack, BinarySearchTree

# Create a linked list
linked_list = SinglyLinkedList()
linked_list.append(10)
linked_list.append(20)
print(linked_list)  # Output: [10, 20]

# Create a stack
stack = Stack()
stack.push(5)
stack.push(10)
print(stack.pop())  # Output: 10

# Create a binary search tree
bst = BinarySearchTree()
bst.insert(5)
bst.insert(3)
bst.insert(7)
print(bst.inorder_traversal())  # Output: [3, 5, 7]
```

## Features

- **Well-Documented**: Each implementation includes detailed documentation and examples
- **Type Hints**: Type annotations for better IDE support and code understanding
- **Comprehensive Tests**: Extensive unit tests for every data structure
- **Performance Focused**: Optimized implementations with efficient algorithms
- **Visualizations**: Documentation includes Mermaid.js diagrams for visual understanding

## Data Structure Properties

| Data Structure | Time Complexity |  |  |  |  | Space Complexity |
|---|---|---|---|---|---|---|
|  | Access | Search | Insertion | Deletion | Traversal |  |
| Array | O(1) | O(n) | O(n) | O(n) | O(n) | O(n) |
| Singly Linked List | O(n) | O(n) | O(1) | O(1) | O(n) | O(n) |
| Doubly Linked List | O(n) | O(n) | O(1) | O(1) | O(n) | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) | O(n) |
| Binary Search Tree | O(log n) - O(n) | O(log n) - O(n) | O(log n) - O(n) | O(log n) - O(n) | O(n) | O(n) |
| AVL Tree | O(log n) | O(log n) | O(log n) | O(log n) | O(n) | O(n) |
| Min/Max Heap | O(n) | O(n) | O(log n) | O(log n) | O(n) | O(n) |
| Bloom Filter | N/A | O(k) | O(k) | N/A | N/A | O(m) |
| Sparse Table | O(1) - O(log n) | N/A | N/A | N/A | O(n) | O(n log n) |

Where:
- k is the number of hash functions (Bloom Filter)
- m is the size of the bit array (Bloom Filter)

## Documentation

Complete documentation is available in the `docs` folder:

- [Basic Data Structures](docs/basic_data_structures.md)
- [Trees](docs/trees.md)
- [Queue Structures](docs/queue_structures.md)
- [Stack Structures](docs/stack_structures.md)
- [Advanced Data Structures](docs/advanced_data_structures.md)

## Resources

- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [Visualgo](https://visualgo.net/en) - Visualizing data structures and algorithms
- [GeeksforGeeks Data Structures](https://www.geeksforgeeks.org/data-structures/)
- [OpenDSA Data Structures and Algorithms](https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/)

