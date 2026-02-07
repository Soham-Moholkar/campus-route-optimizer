"""
BFS and DFS implementations for graph traversal.
Unit 5: Graph Algorithms

Time Complexity:
- BFS: O(V + E) where V = vertices, E = edges
- DFS: O(V + E)

Space Complexity:
- BFS: O(V) for queue
- DFS: O(V) for recursion stack/stack
"""
from typing import List, Dict, Set
from collections import deque


def bfs(graph: Dict[int, List[tuple]], start: int, end: int = None) -> Dict:
    """
    Breadth-First Search traversal.
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        start: Starting node
        end: Optional target node for early termination
    
    Returns:
        Dict with 'visited' order, 'parent' map, and 'distances'
    """
    visited = set()
    queue = deque([start])
    parent = {start: None}
    distance = {start: 0}
    order = []
    
    while queue:
        node = queue.popleft()
        
        if node in visited:
            continue
            
        visited.add(node)
        order.append(node)
        
        if end is not None and node == end:
            break
        
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                if neighbor not in parent:
                    parent[neighbor] = node
                    distance[neighbor] = distance[node] + 1
    
    return {
        "visited": order,
        "parent": parent,
        "distance": distance
    }


def dfs(graph: Dict[int, List[tuple]], start: int, end: int = None) -> Dict:
    """
    Depth-First Search traversal (iterative).
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        start: Starting node
        end: Optional target node for early termination
    
    Returns:
        Dict with 'visited' order, 'parent' map, and 'finish_time'
    """
    visited = set()
    stack = [start]
    parent = {start: None}
    order = []
    
    while stack:
        node = stack.pop()
        
        if node in visited:
            continue
            
        visited.add(node)
        order.append(node)
        
        if end is not None and node == end:
            break
        
        # Add neighbors in reverse order to maintain left-to-right exploration
        neighbors = list(graph.get(node, []))
        for neighbor, _ in reversed(neighbors):
            if neighbor not in visited:
                stack.append(neighbor)
                if neighbor not in parent:
                    parent[neighbor] = node
    
    return {
        "visited": order,
        "parent": parent
    }


def dfs_recursive(graph: Dict[int, List[tuple]], start: int, 
                  visited: Set[int] = None, parent: Dict[int, int] = None,
                  order: List[int] = None) -> Dict:
    """
    Depth-First Search traversal (recursive).
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        start: Starting node
        visited: Set of visited nodes (for recursion)
        parent: Parent map (for recursion)
        order: Visit order (for recursion)
    
    Returns:
        Dict with 'visited' order and 'parent' map
    """
    if visited is None:
        visited = set()
    if parent is None:
        parent = {start: None}
    if order is None:
        order = []
    
    visited.add(start)
    order.append(start)
    
    for neighbor, _ in graph.get(start, []):
        if neighbor not in visited:
            parent[neighbor] = start
            dfs_recursive(graph, neighbor, visited, parent, order)
    
    return {
        "visited": order,
        "parent": parent
    }


def is_connected(graph: Dict[int, List[tuple]], num_nodes: int) -> bool:
    """
    Check if undirected graph is connected using BFS.
    
    Time Complexity: O(V + E)
    """
    if num_nodes == 0:
        return True
    
    result = bfs(graph, 0)
    return len(result["visited"]) == num_nodes


def find_path_bfs(graph: Dict[int, List[tuple]], start: int, end: int) -> List[int]:
    """
    Find path from start to end using BFS (unweighted shortest path).
    
    Args:
        graph: Adjacency list
        start: Start node
        end: End node
    
    Returns:
        List of nodes in path, or empty list if no path exists
    """
    result = bfs(graph, start, end)
    
    if end not in result["parent"]:
        return []
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = result["parent"][current]
    
    path.reverse()
    return path
