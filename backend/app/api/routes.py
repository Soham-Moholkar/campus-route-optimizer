"""
Graph and routing API endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.models.campus import CampusGraph
from app.models.route import RouteRequest, RouteResult
from app.services.graph_service import graph_service
from app.services.crowd_service import crowd_service

router = APIRouter()


class GenerateGraphRequest(BaseModel):
    """Request for generating campus graph."""
    num_nodes: int = Field(default=20, ge=5, le=100, description="Number of buildings")
    edge_probability: float = Field(default=0.3, ge=0.1, le=0.9, description="Edge probability")
    seed: int = Field(default=42, description="Random seed")


class CrowdSimulateRequest(BaseModel):
    """Request for crowd simulation."""
    flow_intensity: float = Field(default=0.5, ge=0.0, le=1.0, description="Flow intensity")
    time_window: str = Field(default="peak", description="Time window: peak, normal, low")
    seed: int = Field(default=42, description="Random seed")


@router.post("/generate/campus_graph", response_model=CampusGraph)
async def generate_campus_graph(request: GenerateGraphRequest):
    """
    Generate a random campus graph.
    
    Returns a connected graph with buildings, walkways, and rooms.
    """
    try:
        graph = graph_service.generate_random_graph(
            num_nodes=request.num_nodes,
            edge_probability=request.edge_probability,
            seed=request.seed
        )
        return graph
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/route/shortest", response_model=RouteResult)
async def compute_shortest_path(request: RouteRequest):
    """
    Compute shortest path between two nodes.
    
    Supports algorithms: dijkstra, floyd_warshall, bfs
    """
    try:
        if graph_service.current_graph is None:
            raise HTTPException(status_code=400, detail="No graph loaded. Generate a graph first.")
        
        # Apply crowd-aware routing if requested
        if request.crowd_mode:
            # Simulate crowd if not done
            if not crowd_service.crowd_weights:
                crowd_service.simulate_crowd(graph_service.current_graph)
            
            # Get dynamic graph
            dynamic_graph = crowd_service.get_dynamic_graph(
                graph_service.adjacency_list,
                alpha=request.crowd_alpha
            )
            
            # Temporarily swap graphs
            original_graph = graph_service.adjacency_list
            graph_service.adjacency_list = dynamic_graph
            
            result = graph_service.compute_shortest_path(request)
            
            # Restore original
            graph_service.adjacency_list = original_graph
            
            result.notes = f"Crowd-aware routing (alpha={request.crowd_alpha})"
        else:
            result = graph_service.compute_shortest_path(request)
        
        return result
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crowd/simulate")
async def simulate_crowd(request: CrowdSimulateRequest):
    """
    Simulate crowd flow on campus.
    
    Updates edge weights based on simulated congestion.
    """
    try:
        if graph_service.current_graph is None:
            raise HTTPException(status_code=400, detail="No graph loaded. Generate a graph first.")
        
        stats = crowd_service.simulate_crowd(
            graph_service.current_graph,
            flow_intensity=request.flow_intensity,
            time_window=request.time_window,
            seed=request.seed
        )
        
        return {
            "message": "Crowd simulation completed",
            "statistics": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph/current")
async def get_current_graph():
    """Get the currently loaded campus graph."""
    if graph_service.current_graph is None:
        raise HTTPException(status_code=404, detail="No graph loaded.")
    
    return graph_service.current_graph


@router.get("/graph/distance_matrix")
async def get_distance_matrix():
    """
    Get all-pairs shortest distance matrix.
    
    Uses Floyd-Warshall (O(V³)) with caching.
    """
    try:
        if graph_service.current_graph is None:
            raise HTTPException(status_code=400, detail="No graph loaded.")
        
        distances = graph_service.get_distance_matrix()
        
        # Convert to list format for JSON
        distance_list = [
            {"from": u, "to": v, "distance": dist}
            for (u, v), dist in distances.items()
        ]
        
        return {
            "num_nodes": len(graph_service.current_graph.nodes),
            "distances": distance_list[:100]  # Limit for response size
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
