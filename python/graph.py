import unittest
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from collections import deque

class Vertex:
    """
    A vertex (node) in a graph.
    
    Attributes:
        value: The value stored in this vertex
        neighbors: Dictionary mapping neighbor vertices to edge weights
    """
    def __init__(self, value: Any):
        """
        Initialize a vertex.
        
        Args:
            value: The value to store in this vertex
        """
        self.value = value
        self.neighbors: Dict[Vertex, float] = {}
        
    def __str__(self) -> str:
        """
        Return the string representation of the vertex.
        """
        return str(self.value)
        
    def __repr__(self) -> str:
        """
        Return the string representation of the vertex.
        """
        return self.__str__()
        
    def add_neighbor(self, neighbor: 'Vertex', weight: float = 1.0) -> None:
        """
        Add a neighbor to this vertex.
        
        Args:
            neighbor: The neighbor vertex to add
            weight: The weight of the edge (default: 1.0)
        """
        self.neighbors[neighbor] = weight
        
    def remove_neighbor(self, neighbor: 'Vertex') -> None:
        """
        Remove a neighbor from this vertex.
        
        Args:
            neighbor: The neighbor vertex to remove
        """
        if neighbor in self.neighbors:
            del self.neighbors[neighbor]
            
    def get_neighbors(self) -> List[Tuple['Vertex', float]]:
        """
        Get all neighbors of this vertex with their edge weights.
        
        Returns:
            List of (neighbor, weight) tuples
        """
        return list(self.neighbors.items())
        
    def has_neighbor(self, neighbor: 'Vertex') -> bool:
        """
        Check if this vertex has a specific neighbor.
        
        Args:
            neighbor: The neighbor vertex to check for
            
        Returns:
            True if the neighbor exists, False otherwise
        """
        return neighbor in self.neighbors

class Graph:
    """
    A graph data structure that can be either directed or undirected.
    Supports weighted edges and various graph operations.
    
    Methods:
        - add_vertex(value) add a vertex
        - add_edge(from_vertex, to_vertex, weight) add an edge
        - remove_vertex(value) remove a vertex
        - remove_edge(from_vertex, to_vertex) remove an edge
        - get_vertex(value) get a vertex by value
        - has_vertex(value) check if a vertex exists
        - has_edge(from_vertex, to_vertex) check if an edge exists
        - get_edge_weight(from_vertex, to_vertex) get edge weight
        - get_vertices() get all vertices
        - get_edges() get all edges
        - clear() remove all vertices and edges
        - bfs(start_value) perform breadth-first search
        - dfs(start_value) perform depth-first search
        - is_connected() check if graph is connected
        - get_shortest_path(start_value, end_value) find shortest path
    """
    def __init__(self, directed: bool = False):
        """
        Initialize an empty graph.
        
        Args:
            directed: Whether this is a directed graph (default: False)
        """
        self.directed = directed
        self.vertices: Dict[Any, Vertex] = {}
        
    def __str__(self) -> str:
        """
        Return the string representation of the graph.
        """
        return f"Graph(directed={self.directed}, vertices={len(self.vertices)})"
        
    def __repr__(self) -> str:
        """
        Return the string representation of the graph.
        """
        return self.__str__()
        
    def add_vertex(self, value: Any) -> Vertex:
        """
        Add a vertex to the graph.
        
        Args:
            value: The value to store in the vertex
            
        Returns:
            The created vertex
        """
        if value in self.vertices:
            return self.vertices[value]
            
        vertex = Vertex(value)
        self.vertices[value] = vertex
        return vertex
        
    def add_edge(self, from_value: Any, to_value: Any, weight: float = 1.0) -> None:
        """
        Add an edge to the graph.
        
        Args:
            from_value: The value of the source vertex
            to_value: The value of the destination vertex
            weight: The weight of the edge (default: 1.0)
        """
        from_vertex = self.add_vertex(from_value)
        to_vertex = self.add_vertex(to_value)
        
        from_vertex.add_neighbor(to_vertex, weight)
        if not self.directed:
            to_vertex.add_neighbor(from_vertex, weight)
            
    def remove_vertex(self, value: Any) -> bool:
        """
        Remove a vertex from the graph.
        
        Args:
            value: The value of the vertex to remove
            
        Returns:
            True if the vertex was removed, False if it wasn't found
        """
        if value not in self.vertices:
            return False
            
        vertex = self.vertices[value]
        
        # Remove edges to this vertex from all other vertices
        for other_vertex in self.vertices.values():
            if other_vertex != vertex:
                other_vertex.remove_neighbor(vertex)
                
        del self.vertices[value]
        return True
        
    def remove_edge(self, from_value: Any, to_value: Any) -> bool:
        """
        Remove an edge from the graph.
        
        Args:
            from_value: The value of the source vertex
            to_value: The value of the destination vertex
            
        Returns:
            True if the edge was removed, False if it wasn't found
        """
        if from_value not in self.vertices or to_value not in self.vertices:
            return False
            
        from_vertex = self.vertices[from_value]
        to_vertex = self.vertices[to_value]
        
        if not from_vertex.has_neighbor(to_vertex):
            return False
            
        from_vertex.remove_neighbor(to_vertex)
        if not self.directed:
            to_vertex.remove_neighbor(from_vertex)
        return True
        
    def get_vertex(self, value: Any) -> Optional[Vertex]:
        """
        Get a vertex by its value.
        
        Args:
            value: The value of the vertex to get
            
        Returns:
            The vertex if found, None otherwise
        """
        return self.vertices.get(value)
        
    def has_vertex(self, value: Any) -> bool:
        """
        Check if a vertex exists in the graph.
        
        Args:
            value: The value of the vertex to check for
            
        Returns:
            True if the vertex exists, False otherwise
        """
        return value in self.vertices
        
    def has_edge(self, from_value: Any, to_value: Any) -> bool:
        """
        Check if an edge exists in the graph.
        
        Args:
            from_value: The value of the source vertex
            to_value: The value of the destination vertex
            
        Returns:
            True if the edge exists, False otherwise
        """
        if from_value not in self.vertices or to_value not in self.vertices:
            return False
            
        from_vertex = self.vertices[from_value]
        to_vertex = self.vertices[to_value]
        return from_vertex.has_neighbor(to_vertex)
        
    def get_edge_weight(self, from_value: Any, to_value: Any) -> Optional[float]:
        """
        Get the weight of an edge.
        
        Args:
            from_value: The value of the source vertex
            to_value: The value of the destination vertex
            
        Returns:
            The edge weight if found, None otherwise
        """
        if from_value not in self.vertices or to_value not in self.vertices:
            return None
            
        from_vertex = self.vertices[from_value]
        to_vertex = self.vertices[to_value]
        return from_vertex.neighbors.get(to_vertex)
        
    def get_vertices(self) -> List[Any]:
        """
        Get all vertex values in the graph.
        
        Returns:
            List of vertex values
        """
        return list(self.vertices.keys())
        
    def get_edges(self) -> List[Tuple[Any, Any, float]]:
        """
        Get all edges in the graph.
        
        Returns:
            List of (from_value, to_value, weight) tuples
        """
        edges = []
        for from_value, from_vertex in self.vertices.items():
            for to_vertex, weight in from_vertex.neighbors.items():
                to_value = to_vertex.value
                if self.directed or from_value <= to_value:  # Avoid duplicate edges in undirected graphs
                    edges.append((from_value, to_value, weight))
        return edges
        
    def clear(self) -> None:
        """
        Remove all vertices and edges from the graph.
        """
        self.vertices.clear()
        
    def bfs(self, start_value: Any) -> List[Any]:
        """
        Perform breadth-first search starting from a vertex.
        
        Args:
            start_value: The value of the starting vertex
            
        Returns:
            List of vertex values in BFS order
        """
        if start_value not in self.vertices:
            return []
            
        visited = set()
        queue = deque([start_value])
        result = []
        
        while queue:
            value = queue.popleft()
            if value in visited:
                continue
                
            visited.add(value)
            result.append(value)
            
            vertex = self.vertices[value]
            for neighbor, _ in vertex.get_neighbors():
                if neighbor.value not in visited:
                    queue.append(neighbor.value)
                    
        return result
        
    def dfs(self, start_value: Any) -> List[Any]:
        """
        Perform depth-first search starting from a vertex.
        
        Args:
            start_value: The value of the starting vertex
            
        Returns:
            List of vertex values in DFS order
        """
        if start_value not in self.vertices:
            return []
            
        visited = set()
        result = []
        
        def dfs_recursive(value: Any) -> None:
            if value in visited:
                return
                
            visited.add(value)
            result.append(value)
            
            vertex = self.vertices[value]
            for neighbor, _ in vertex.get_neighbors():
                dfs_recursive(neighbor.value)
                
        dfs_recursive(start_value)
        return result
        
    def is_connected(self) -> bool:
        """
        Check if the graph is connected.
        
        Returns:
            True if the graph is connected, False otherwise
        """
        if not self.vertices:
            return True
            
        start_value = next(iter(self.vertices))
        visited = set(self.bfs(start_value))
        return len(visited) == len(self.vertices)
        
    def get_shortest_path(self, start_value: Any, end_value: Any) -> Optional[List[Any]]:
        """
        Find the shortest path between two vertices using Dijkstra's algorithm.
        
        Args:
            start_value: The value of the starting vertex
            end_value: The value of the ending vertex
            
        Returns:
            List of vertex values in the shortest path, or None if no path exists
        """
        if start_value not in self.vertices or end_value not in self.vertices:
            return None
            
        # Initialize distances and previous vertices
        distances = {value: float('inf') for value in self.vertices}
        previous = {value: None for value in self.vertices}
        distances[start_value] = 0
        
        # Initialize unvisited set
        unvisited = set(self.vertices.keys())
        
        while unvisited:
            # Find vertex with minimum distance
            current_value = min(unvisited, key=lambda v: distances[v])
            if current_value == end_value:
                break
                
            unvisited.remove(current_value)
            current_vertex = self.vertices[current_value]
            
            # Update distances to neighbors
            for neighbor, weight in current_vertex.get_neighbors():
                neighbor_value = neighbor.value
                if neighbor_value in unvisited:
                    new_distance = distances[current_value] + weight
                    if new_distance < distances[neighbor_value]:
                        distances[neighbor_value] = new_distance
                        previous[neighbor_value] = current_value
                        
        # Check if path exists
        if distances[end_value] == float('inf'):
            return None
            
        # Reconstruct path
        path = []
        current_value = end_value
        while current_value is not None:
            path.append(current_value)
            current_value = previous[current_value]
        return list(reversed(path))


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        
    def test_init(self):
        self.assertFalse(self.graph.directed)
        self.assertEqual(len(self.graph.vertices), 0)
        
    def test_add_vertex(self):
        vertex = self.graph.add_vertex("A")
        self.assertEqual(vertex.value, "A")
        self.assertEqual(len(self.graph.vertices), 1)
        
        # Test adding duplicate vertex
        vertex2 = self.graph.add_vertex("A")
        self.assertEqual(vertex2, vertex)
        self.assertEqual(len(self.graph.vertices), 1)
        
    def test_add_edge(self):
        self.graph.add_edge("A", "B")
        self.assertEqual(len(self.graph.vertices), 2)
        self.assertTrue(self.graph.has_edge("A", "B"))
        self.assertTrue(self.graph.has_edge("B", "A"))  # Undirected graph
        
        # Test weighted edge
        self.graph.add_edge("B", "C", 2.0)
        self.assertEqual(self.graph.get_edge_weight("B", "C"), 2.0)
        self.assertEqual(self.graph.get_edge_weight("C", "B"), 2.0)  # Undirected graph
        
    def test_remove_vertex(self):
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        
        self.assertTrue(self.graph.remove_vertex("B"))
        self.assertEqual(len(self.graph.vertices), 2)
        self.assertFalse(self.graph.has_edge("A", "B"))
        self.assertFalse(self.graph.has_edge("B", "C"))
        
    def test_remove_edge(self):
        self.graph.add_edge("A", "B")
        self.assertTrue(self.graph.remove_edge("A", "B"))
        self.assertFalse(self.graph.has_edge("A", "B"))
        self.assertFalse(self.graph.has_edge("B", "A"))  # Undirected graph
        
    def test_get_vertex(self):
        self.graph.add_vertex("A")
        vertex = self.graph.get_vertex("A")
        self.assertEqual(vertex.value, "A")
        self.assertIsNone(self.graph.get_vertex("B"))
        
    def test_has_vertex(self):
        self.graph.add_vertex("A")
        self.assertTrue(self.graph.has_vertex("A"))
        self.assertFalse(self.graph.has_vertex("B"))
        
    def test_has_edge(self):
        self.graph.add_edge("A", "B")
        self.assertTrue(self.graph.has_edge("A", "B"))
        self.assertTrue(self.graph.has_edge("B", "A"))  # Undirected graph
        self.assertFalse(self.graph.has_edge("A", "C"))
        
    def test_get_edge_weight(self):
        self.graph.add_edge("A", "B", 2.0)
        self.assertEqual(self.graph.get_edge_weight("A", "B"), 2.0)
        self.assertEqual(self.graph.get_edge_weight("B", "A"), 2.0)  # Undirected graph
        self.assertIsNone(self.graph.get_edge_weight("A", "C"))
        
    def test_get_vertices(self):
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        vertices = self.graph.get_vertices()
        self.assertEqual(set(vertices), {"A", "B", "C"})
        
    def test_get_edges(self):
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("B", "C", 2.0)
        edges = self.graph.get_edges()
        self.assertEqual(set(edges), {
            ("A", "B", 1.0),
            ("B", "A", 1.0),
            ("B", "C", 2.0),
            ("C", "B", 2.0)
        })
        
    def test_clear(self):
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        self.graph.clear()
        self.assertEqual(len(self.graph.vertices), 0)
        
    def test_bfs(self):
        self.graph.add_edge("A", "B")
        self.graph.add_edge("A", "C")
        self.graph.add_edge("B", "D")
        self.graph.add_edge("C", "E")
        
        bfs_result = self.graph.bfs("A")
        self.assertEqual(bfs_result, ["A", "B", "C", "D", "E"])
        
    def test_dfs(self):
        self.graph.add_edge("A", "B")
        self.graph.add_edge("A", "C")
        self.graph.add_edge("B", "D")
        self.graph.add_edge("C", "E")
        
        dfs_result = self.graph.dfs("A")
        self.assertEqual(dfs_result, ["A", "B", "D", "C", "E"])
        
    def test_is_connected(self):
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        self.assertTrue(self.graph.is_connected())
        
        self.graph.add_vertex("D")
        self.assertFalse(self.graph.is_connected())
        
    def test_get_shortest_path(self):
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("B", "C", 2.0)
        self.graph.add_edge("A", "C", 4.0)
        
        path = self.graph.get_shortest_path("A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        
        # Test disconnected graph
        self.graph.add_vertex("D")
        self.assertIsNone(self.graph.get_shortest_path("A", "D"))
        
    def test_directed_graph(self):
        directed_graph = Graph(directed=True)
        directed_graph.add_edge("A", "B")
        directed_graph.add_edge("B", "C")
        
        self.assertTrue(directed_graph.has_edge("A", "B"))
        self.assertFalse(directed_graph.has_edge("B", "A"))
        self.assertTrue(directed_graph.has_edge("B", "C"))
        self.assertFalse(directed_graph.has_edge("C", "B"))
        
        edges = directed_graph.get_edges()
        self.assertEqual(set(edges), {
            ("A", "B", 1.0),
            ("B", "C", 1.0)
        })
        
    def test_complex_graph(self):
        # Create a complex graph with multiple paths
        self.graph.add_edge("A", "B", 1.0)
        self.graph.add_edge("B", "C", 2.0)
        self.graph.add_edge("A", "C", 4.0)
        self.graph.add_edge("B", "D", 3.0)
        self.graph.add_edge("C", "D", 1.0)
        
        # Test BFS
        bfs_result = self.graph.bfs("A")
        self.assertEqual(bfs_result, ["A", "B", "C", "D"])
        
        # Test DFS
        dfs_result = self.graph.dfs("A")
        self.assertEqual(dfs_result, ["A", "B", "C", "D"])
        
        # Test shortest path
        path = self.graph.get_shortest_path("A", "D")
        self.assertEqual(path, ["A", "B", "D"])
        
        # Test edge weights
        self.assertEqual(self.graph.get_edge_weight("A", "B"), 1.0)
        self.assertEqual(self.graph.get_edge_weight("B", "C"), 2.0)
        self.assertEqual(self.graph.get_edge_weight("A", "C"), 4.0)
        
        # Test removing edges
        self.assertTrue(self.graph.remove_edge("B", "C"))
        self.assertFalse(self.graph.has_edge("B", "C"))
        self.assertFalse(self.graph.has_edge("C", "B"))
        
        # Test removing vertices
        self.assertTrue(self.graph.remove_vertex("C"))
        self.assertEqual(len(self.graph.vertices), 3)
        self.assertFalse(self.graph.has_edge("A", "C"))
        self.assertFalse(self.graph.has_edge("B", "C"))
        self.assertFalse(self.graph.has_edge("C", "D"))


if __name__ == '__main__':
    unittest.main() 