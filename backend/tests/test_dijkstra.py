"""
Unit tests for Dijkstra's algorithm.
"""
import pytest
from app.algorithms.graph.dijkstra import dijkstra, dijkstra_path


def test_dijkstra_simple():
    """Test Dijkstra on a simple graph."""
    # Simple graph: 0 -> 1 (weight 4), 0 -> 2 (weight 2), 2 -> 1 (weight 1)
    graph = {
        0: [(1, 4), (2, 2)],
        1: [],
        2: [(1, 1)]
    }
    
    result = dijkstra(graph, 0)
    
    assert result["distances"][0] == 0
    assert result["distances"][1] == 3  # Via 2
    assert result["distances"][2] == 2


def test_dijkstra_path():
    """Test Dijkstra path reconstruction."""
    graph = {
        0: [(1, 4), (2, 2)],
        1: [(3, 1)],
        2: [(1, 1), (3, 5)],
        3: []
    }
    
    path, distance = dijkstra_path(graph, 0, 3)
    
    assert distance == 4  # 0 -> 2 -> 1 -> 3
    assert path == [0, 2, 1, 3]


def test_dijkstra_unreachable():
    """Test Dijkstra with unreachable node."""
    graph = {
        0: [(1, 1)],
        1: [],
        2: [(3, 1)],
        3: []
    }
    
    path, distance = dijkstra_path(graph, 0, 3)
    
    assert distance == float('inf')
    assert path == []


def test_dijkstra_single_node():
    """Test Dijkstra with single node."""
    graph = {0: []}
    
    result = dijkstra(graph, 0)
    
    assert result["distances"][0] == 0


def test_dijkstra_cycle():
    """Test Dijkstra with cycles."""
    graph = {
        0: [(1, 1)],
        1: [(2, 1)],
        2: [(0, 1), (3, 1)],
        3: []
    }
    
    result = dijkstra(graph, 0)
    
    assert result["distances"][0] == 0
    assert result["distances"][1] == 1
    assert result["distances"][2] == 2
    assert result["distances"][3] == 3
