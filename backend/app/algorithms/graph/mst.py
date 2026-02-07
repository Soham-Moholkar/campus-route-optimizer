"""
Kruskal's Algorithm for Minimum Spanning Tree.
Unit 5: Graph Algorithms (Greedy approach)

Time Complexity: O(E log V) with Union-Find
Space Complexity: O(V + E)

Useful for "Campus Expansion Planning" - finding minimum cost walkway network.
"""
from typing import List, Tuple, Dict


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure.
    
    Supports near-constant time union and find operations with
    path compression and union by rank.
    """
    
    def __init__(self, n: int):
        """Initialize n disjoint sets."""
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x: int) -> int:
        """
        Find the root of the set containing x.
        Uses path compression for optimization.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        Unite the sets containing x and y.
        Returns True if they were in different sets (union performed).
        Uses union by rank for optimization.
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in the same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True


def kruskal_mst(edges: List[Tuple[int, int, float]], num_nodes: int) -> Dict:
    """
    Kruskal's algorithm for Minimum Spanning Tree.
    
    Args:
        edges: List of (u, v, weight) tuples (undirected edges)
        num_nodes: Total number of nodes
    
    Returns:
        Dict with 'mst_edges', 'total_weight', and 'is_connected'
    """
    # Sort edges by weight (greedy choice)
    sorted_edges = sorted(edges, key=lambda e: e[2])
    
    uf = UnionFind(num_nodes)
    mst_edges = []
    total_weight = 0.0
    
    for u, v, weight in sorted_edges:
        # Try to add edge if it doesn't create a cycle
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            # MST complete when we have (n-1) edges
            if len(mst_edges) == num_nodes - 1:
                break
    
    # Check if graph is connected (MST has n-1 edges)
    is_connected = len(mst_edges) == num_nodes - 1
    
    return {
        "mst_edges": mst_edges,
        "total_weight": total_weight,
        "is_connected": is_connected,
        "num_components": num_nodes - len(mst_edges)  # Remaining components
    }


def kruskal_from_adjacency(graph: Dict[int, List[Tuple[int, float]]], 
                          num_nodes: int) -> Dict:
    """
    Kruskal's MST from adjacency list representation.
    
    Args:
        graph: Adjacency list (assumes undirected graph)
        num_nodes: Total number of nodes
    
    Returns:
        MST result dict
    """
    # Convert adjacency list to edge list
    edges = []
    seen = set()
    
    for u in graph:
        for v, weight in graph[u]:
            # Avoid duplicate edges in undirected graph
            edge_key = (min(u, v), max(u, v))
            if edge_key not in seen:
                seen.add(edge_key)
                edges.append((u, v, weight))
    
    return kruskal_mst(edges, num_nodes)


def campus_expansion_plan(current_edges: List[Tuple[int, int, float]], 
                          potential_edges: List[Tuple[int, int, float]], 
                          num_nodes: int) -> Dict:
    """
    Campus expansion planning: Given existing walkways and potential new ones,
    find minimum cost additions to ensure full connectivity.
    
    Args:
        current_edges: Existing walkways
        potential_edges: Potential new walkways to build
        num_nodes: Number of buildings
    
    Returns:
        Dict with edges to build, total cost, and full MST
    """
    # First, find what's already connected
    uf = UnionFind(num_nodes)
    existing_weight = 0.0
    
    for u, v, weight in current_edges:
        uf.union(u, v)
        existing_weight += weight
    
    # Sort potential edges by cost
    sorted_potential = sorted(potential_edges, key=lambda e: e[2])
    
    edges_to_build = []
    total_new_cost = 0.0
    
    # Greedily add cheapest edges that connect components
    for u, v, weight in sorted_potential:
        if uf.union(u, v):
            edges_to_build.append((u, v, weight))
            total_new_cost += weight
            
            if len(current_edges) + len(edges_to_build) == num_nodes - 1:
                break
    
    is_fully_connected = len(current_edges) + len(edges_to_build) == num_nodes - 1
    
    return {
        "edges_to_build": edges_to_build,
        "new_construction_cost": total_new_cost,
        "existing_cost": existing_weight,
        "total_cost": existing_weight + total_new_cost,
        "is_fully_connected": is_fully_connected
    }
