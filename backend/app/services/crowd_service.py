"""
Crowd simulation service for crowd-aware routing.
"""
from typing import Dict, Tuple, List
import random
from app.models.campus import CampusGraph


class CrowdService:
    """Service for simulating crowd congestion on campus."""
    
    def __init__(self):
        self.crowd_weights: Dict[Tuple[int, int], float] = {}
        self.usage_counts: Dict[Tuple[int, int], int] = {}
    
    def simulate_crowd(self, graph: CampusGraph, flow_intensity: float = 0.5,
                      time_window: str = "peak", seed: int = 42) -> Dict:
        """
        Simulate crowd flow on campus edges.
        
        Args:
            graph: Campus graph
            flow_intensity: Flow intensity (0-1)
            time_window: "peak", "normal", or "low"
            seed: Random seed
        
        Returns:
            Dict with crowd statistics
        """
        random.seed(seed)
        
        # Reset
        self.usage_counts = {}
        self.crowd_weights = {}
        
        # Base usage depends on time window
        base_multiplier = {
            "peak": 2.0,
            "normal": 1.0,
            "low": 0.3
        }.get(time_window, 1.0)
        
        # Simulate random flows
        num_flows = int(len(graph.nodes) * flow_intensity * base_multiplier * 10)
        
        for _ in range(num_flows):
            # Pick random source and destination
            source = random.choice(graph.nodes)
            dest = random.choice(graph.nodes)
            
            if source.id == dest.id:
                continue
            
            # Simulate path (for simplicity, increment random edges)
            # In reality, would use shortest path
            edges_in_flow = random.sample(graph.edges, min(3, len(graph.edges)))
            
            for edge in edges_in_flow:
                key = (edge.u, edge.v)
                self.usage_counts[key] = self.usage_counts.get(key, 0) + 1
        
        # Compute crowd weights
        max_usage = max(self.usage_counts.values()) if self.usage_counts else 1
        
        for edge in graph.edges:
            key = (edge.u, edge.v)
            usage = self.usage_counts.get(key, 0)
            
            # Crowd penalty as fraction of base weight
            crowd_factor = (usage / max_usage) if max_usage > 0 else 0
            self.crowd_weights[key] = edge.base_weight * (1 + crowd_factor)
        
        return {
            "total_flows": num_flows,
            "max_usage": max_usage,
            "avg_usage": sum(self.usage_counts.values()) / max(len(self.usage_counts), 1),
            "num_edges_affected": len(self.usage_counts)
        }
    
    def get_dynamic_graph(self, base_graph: Dict[int, List[Tuple[int, float]]], 
                         alpha: float = 0.3) -> Dict[int, List[Tuple[int, float]]]:
        """
        Get graph with dynamic crowd-aware weights.
        
        Args:
            base_graph: Base adjacency list
            alpha: Crowd penalty weight (0-1)
        
        Returns:
            Adjacency list with updated weights
        """
        dynamic_graph = {}
        
        for u in base_graph:
            dynamic_graph[u] = []
            for v, base_weight in base_graph[u]:
                crowd_weight = self.crowd_weights.get((u, v), base_weight)
                # Blend base and crowd weights
                final_weight = (1 - alpha) * base_weight + alpha * crowd_weight
                dynamic_graph[u].append((v, final_weight))
        
        return dynamic_graph


# Global instance
crowd_service = CrowdService()
