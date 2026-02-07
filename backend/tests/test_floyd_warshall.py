"""
Unit tests for Floyd-Warshall algorithm.
"""
import pytest
from app.algorithms.graph.floyd_warshall import floyd_warshall, floyd_warshall_with_paths


def test_floyd_warshall_simple():
    """Test Floyd-Warshall on a simple graph."""
    graph = {
        0: [(1, 4), (2, 2)],
        1: [],
        2: [(1, 1)]
    }
    
    dist, next_matrix = floyd_warshall(graph, 3)
    
    assert dist[0][0] == 0
    assert dist[0][1] == 3  # Via 2
    assert dist[0][2] == 2
    assert dist[1][0] == float('inf')
    assert dist[2][1] == 1


def test_floyd_warshall_paths():
    """Test Floyd-Warshall with path reconstruction."""
    graph = {
        0: [(1, 4), (2, 2)],
        1: [(3, 1)],
        2: [(1, 1), (3, 5)],
        3: []
    }
    
    fw = floyd_warshall_with_paths(graph, 4)
    path, distance = fw["get_path"](0, 3)
    
    assert distance == 4
    assert path == [0, 2, 1, 3]


def test_floyd_warshall_all_pairs():
    """Test Floyd-Warshall computes all pairs."""
    graph = {
        0: [(1, 1)],
        1: [(2, 1)],
        2: []
    }
    
    dist, _ = floyd_warshall(graph, 3)
    
    # Check all pairs
    assert dist[0][1] == 1
    assert dist[0][2] == 2
    assert dist[1][2] == 1


def test_floyd_warshall_disconnected():
    """Test Floyd-Warshall with disconnected components."""
    graph = {
        0: [(1, 1)],
        1: [],
        2: [(3, 1)],
        3: []
    }
    
    dist, _ = floyd_warshall(graph, 4)
    
    assert dist[0][1] == 1
    assert dist[0][2] == float('inf')
    assert dist[2][3] == 1
    assert dist[0][3] == float('inf')
