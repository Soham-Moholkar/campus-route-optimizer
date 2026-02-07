"""
Dijkstra's Algorithm for Single-Source Shortest Paths.
Unit 5: Graph Algorithms

Time Complexity: O((V + E) log V) with binary heap
Space Complexity: O(V)

Implementation uses a min-heap (priority queue) for efficient extraction.
"""
import heapq
from typing import Dict, List, Tuple, Optional


def dijkstra(graph: Dict[int, List[Tuple[int, float]]], start: int, 
             end: Optional[int] = None) -> Dict:
    """
    Dijkstra's shortest path algorithm.
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        start: Starting node
        end: Optional target node for early termination
    
    Returns:
        Dict with 'distances', 'parent', and 'visited' nodes
    """
    # Initialize distances to infinity
    distances = {node: float('inf') for node in graph.keys()}
    distances[start] = 0
    
    # Parent map for path reconstruction
    parent = {start: None}
    
    # Priority queue: (distance, node)
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        # Skip if already visited
        if current in visited:
            continue
        
        visited.add(current)
        
        # Early termination if we reached the target
        if end is not None and current == end:
            break
        
        # Skip if we found a better path already
        if current_dist > distances[current]:
            continue
        
        # Explore neighbors
        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue
            
            distance = current_dist + weight
            
            # Relaxation step
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))
    
    return {
        "distances": distances,
        "parent": parent,
        "visited": list(visited)
    }


def dijkstra_path(graph: Dict[int, List[Tuple[int, float]]], 
                  start: int, end: int) -> Tuple[List[int], float]:
    """
    Get shortest path and distance from start to end using Dijkstra.
    
    Args:
        graph: Adjacency list
        start: Start node
        end: End node
    
    Returns:
        Tuple of (path as list of nodes, total distance)
    """
    result = dijkstra(graph, start, end)
    
    # Check if end is reachable
    if result["distances"][end] == float('inf'):
        return ([], float('inf'))
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = result["parent"].get(current)
    
    path.reverse()
    
    return (path, result["distances"][end])


def dijkstra_all_pairs_from_source(graph: Dict[int, List[Tuple[int, float]]], 
                                    start: int) -> Dict[int, Tuple[List[int], float]]:
    """
    Get shortest paths from start to all other nodes.
    
    Args:
        graph: Adjacency list
        start: Start node
    
    Returns:
        Dict {node: (path, distance)}
    """
    result = dijkstra(graph, start)
    paths = {}
    
    for node in graph.keys():
        if result["distances"][node] == float('inf'):
            paths[node] = ([], float('inf'))
        else:
            # Reconstruct path
            path = []
            current = node
            while current is not None:
                path.append(current)
                current = result["parent"].get(current)
            path.reverse()
            paths[node] = (path, result["distances"][node])
    
    return paths


def dijkstra_multi_target(graph: Dict[int, List[Tuple[int, float]]], 
                          start: int, targets: List[int]) -> Dict[int, Tuple[List[int], float]]:
    """
    Optimized Dijkstra for multiple targets.
    Stops when all targets are visited.
    
    Args:
        graph: Adjacency list
        start: Start node
        targets: List of target nodes
    
    Returns:
        Dict {target: (path, distance)}
    """
    distances = {node: float('inf') for node in graph.keys()}
    distances[start] = 0
    parent = {start: None}
    pq = [(0, start)]
    visited = set()
    
    targets_set = set(targets)
    found_targets = set()
    
    while pq and len(found_targets) < len(targets_set):
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current in targets_set:
            found_targets.add(current)
        
        if current_dist > distances[current]:
            continue
        
        for neighbor, weight in graph.get(current, []):
            if neighbor in visited:
                continue
            
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstruct paths for targets
    results = {}
    for target in targets:
        if distances[target] == float('inf'):
            results[target] = ([], float('inf'))
        else:
            path = []
            current = target
            while current is not None:
                path.append(current)
                current = parent.get(current)
            path.reverse()
            results[target] = (path, distances[target])
    
    return results
