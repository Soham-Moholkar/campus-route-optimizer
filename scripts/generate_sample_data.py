"""
Generate sample campus data.
Creates a random campus graph and saves to JSON.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.services.graph_service import graph_service
import json


def main():
    """Generate sample campus graph."""
    print("Generating sample campus graph...")
    
    graph = graph_service.generate_random_graph(
        num_nodes=20,
        edge_probability=0.35,
        seed=42
    )
    
    # Save to JSON
    output_path = os.path.join("backend", "app", "data", "generated_campus.json")
    
    with open(output_path, "w") as f:
        json.dump(graph.model_dump(), f, indent=2)
    
    print(f"✓ Generated graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
    print(f"✓ Saved to {output_path}")
    print(f"✓ Generated {len(graph.rooms)} rooms")


if __name__ == "__main__":
    main()
