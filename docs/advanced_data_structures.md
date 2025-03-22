# Advanced Data Structures

This document covers advanced data structures that provide efficient solutions for specific types of problems.

## Bloom Filter

A Bloom filter is a space-efficient probabilistic data structure used to test whether an element is a member of a set.

### Explanation

Bloom filters allow you to quickly check if an element might be in a set or is definitely not in the set. They may produce false positives (incorrectly reporting that an element is in the set) but never false negatives. This trade-off allows for very compact representation of sets, using significantly less memory than storing all elements.

### Visual Representation

```mermaid
graph TD
    subgraph "Bloom Filter"
    A["Bit Array: 0 0 0 0 0 0 0 0 0 0"]
    end
    
    B["Add 'apple'"] --> C["Hash Functions"]
    C --> D["Set bits 1, 4, 7"]
    D --> E["Bit Array: 1 0 0 0 1 0 0 1 0 0"]
    
    F["Check 'apple'"] --> G["Hash Functions"]
    G --> H["Check bits 1, 4, 7"]
    H --> I["All bits set? Yes - Might be in set"]
    
    J["Check 'banana'"] --> K["Hash Functions"]
    K --> L["Check bits 2, 3, 9"]
    L --> M["All bits set? No - Definitely not in set"]
```

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Add       | O(k)           |
| Contains  | O(k)           |
| Union     | O(m)           |

Where:
- k is the number of hash functions
- m is the size of the bit array

### Space Complexity

O(m) where m is the size of the bit array. For a desired false positive rate p and n elements, optimal size is:

m = -n ln(p) / (ln(2)²)

### Implementation Notes

Our implementation:
- Automatically calculates optimal bit array size and number of hash functions
- Uses MurmurHash3 for efficient hashing
- Supports union operations and false positive rate calculation
- Allows custom hash functions

### External Resources

- [Bloom Filter - GeeksforGeeks](https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/)
- [Bloom Filters by Example](https://llimllib.github.io/bloomfilter-tutorial/)
- [Interactive Bloom Filter Visualization](https://www.jasondavies.com/bloomfilter/)

## Sparse Table

A sparse table is a data structure that answers range queries efficiently, especially for static arrays.

### Explanation

Sparse tables precompute results for ranges of powers of two, allowing for O(1) queries for idempotent operations (like min, max, gcd) and O(log n) queries for non-idempotent operations (like sum). They're particularly useful when you have a static array with many range queries.

### Visual Representation

```mermaid
graph TD
    subgraph "Sparse Table for Range Minimum Queries"
    A["Original Array: [5, 2, 8, 1, 9, 3, 7, 4]"]
    A --> B["Range length 1 (2^0):<br>[5, 2, 8, 1, 9, 3, 7, 4]"]
    B --> C["Range length 2 (2^1):<br>[2, 2, 1, 1, 3, 3, 4, -]"]
    C --> D["Range length 4 (2^2):<br>[1, 1, 1, 1, 3, -, -, -]"]
    D --> E["Range length 8 (2^3):<br>[1, -, -, -, -, -, -, -]"]
    end
    
    F["Query min(2, 5)"] --> G["Find largest power of 2 ≤ length"]
    G --> H["length = 4, k = 2 (2^2)"]
    H --> I["Combine ranges: min(min(2, 2+2^2-1), min(5-2^2+1, 5))"]
    I --> J["min(table[2][2], table[2][3]) = min(1, 1) = 1"]
```

### Time Complexity

| Operation          | Time Complexity  |
|--------------------|-----------------|
| Construction       | O(n log n)      |
| Idempotent Query   | O(1)            |
| Non-idempotent Query | O(log n)      |

### Space Complexity

O(n log n) where n is the length of the array.

### Implementation Notes

Our implementation:
- Supports both idempotent and non-idempotent operations
- Optimizes query methods based on the operation type
- Provides validation methods for input ranges

### External Resources

- [Sparse Table - CP Algorithms](https://cp-algorithms.com/data_structures/sparse-table.html)
- [Range Queries with Sparse Table](https://www.geeksforgeeks.org/sparse-table/)
- [Sparse Table Tutorial](https://www.hackerearth.com/practice/notes/sparse-table/)

## Use Cases Comparison

| Data Structure | Best For | Advantages | Limitations |
|----------------|----------|------------|-------------|
| Bloom Filter | Membership testing with space constraints | Very space efficient, constant time operations | Cannot store actual elements, false positives possible |
| Sparse Table | Static range queries | O(1) query time for idempotent operations | Immutable array, O(n log n) preprocessing |
