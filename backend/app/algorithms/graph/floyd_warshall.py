"""
Floyd-Warshall Algorithm for All-Pairs Shortest Paths.
Unit 5: Graph Algorithms

Time Complexity: O(V³)
Space Complexity: O(V²)

Computes shortest paths between all pairs of vertices.
Can detect negative cycles.
"""
from typing import Dict, List, Tuple, Optional


def floyd_warshall(graph: Dict[int, List[Tuple[int, float]]], 
                   num_nodes: int) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
    """
    Floyd-Warshall all-pairs shortest path algorithm.
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        num_nodes: Total number of nodes (0 to num_nodes-1)
    
    Returns:
        Tuple of (distance matrix, next matrix for path reconstruction)
    """
    INF = float('inf')
    
    # Initialize distance and next matrices
    dist = [[INF] * num_nodes for _ in range(num_nodes)]
    next_node = [[None] * num_nodes for _ in range(num_nodes)]
    
    # Distance from node to itself is 0
    for i in range(num_nodes):
        dist[i][i] = 0
        next_node[i][i] = i
    
    # Fill initial distances from edges
    for u in graph:
        for v, weight in graph[u]:
            dist[u][v] = weight
            next_node[u][v] = v
    
    # Floyd-Warshall main loop
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
    
    # Check for negative cycles
    for i in range(num_nodes):
        if dist[i][i] < 0:
            raise ValueError(f"Negative cycle detected at node {i}")
    
    return dist, next_node


def reconstruct_path(next_matrix: List[List[Optional[int]]], 
                     start: int, end: int) -> List[int]:
    """
    Reconstruct path from start to end using next matrix.
    
    Args:
        next_matrix: Next node matrix from Floyd-Warshall
        start: Start node
        end: End node
    
    Returns:
        List of nodes in path, or empty list if no path exists
    """
    if next_matrix[start][end] is None:
        return []
    
    path = [start]
    current = start
    
    while current != end:
        current = next_matrix[current][end]
        if current is None:
            return []
        path.append(current)
    
    return path


def floyd_warshall_with_paths(graph: Dict[int, List[Tuple[int, float]]], 
                               num_nodes: int) -> Dict:
    """
    Floyd-Warshall with convenient path reconstruction.
    
    Args:
        graph: Adjacency list
        num_nodes: Total number of nodes
    
    Returns:
        Dict with 'distances' matrix, 'next' matrix, and helper method 'get_path'
    """
    dist, next_matrix = floyd_warshall(graph, num_nodes)
    
    def get_path(start: int, end: int) -> Tuple[List[int], float]:
        """Get path and distance from start to end."""
        if dist[start][end] == float('inf'):
            return ([], float('inf'))
        
        path = reconstruct_path(next_matrix, start, end)
        return (path, dist[start][end])
    
    return {
        "distances": dist,
        "next": next_matrix,
        "get_path": get_path
    }


def floyd_warshall_sparse(edges: List[Tuple[int, int, float]], 
                          num_nodes: int) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
    """
    Floyd-Warshall optimized for sparse graph representation.
    
    Args:
        edges: List of (u, v, weight) tuples
        num_nodes: Total number of nodes
    
    Returns:
        Tuple of (distance matrix, next matrix)
    """
    # Convert to adjacency list first
    graph = {i: [] for i in range(num_nodes)}
    for u, v, weight in edges:
        graph[u].append((v, weight))
    
    return floyd_warshall(graph, num_nodes)


def transitive_closure(graph: Dict[int, List[Tuple[int, float]]], 
                       num_nodes: int) -> List[List[bool]]:
    """
    Compute transitive closure (reachability matrix) using Floyd-Warshall.
    
    Time Complexity: O(V³)
    
    Args:
        graph: Adjacency list
        num_nodes: Total number of nodes
    
    Returns:
        2D boolean matrix where reach[i][j] = True if j is reachable from i
    """
    reach = [[False] * num_nodes for _ in range(num_nodes)]
    
    # Every node can reach itself
    for i in range(num_nodes):
        reach[i][i] = True
    
    # Mark direct edges as reachable
    for u in graph:
        for v, _ in graph[u]:
            reach[u][v] = True
    
    # Floyd-Warshall style propagation
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    
    return reach
