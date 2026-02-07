"""
Routing data models.
Represents path finding requests and results.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class RouteSegment(BaseModel):
    """A segment of a route between two nodes."""
    from_node: int = Field(..., description="Source node ID")
    to_node: int = Field(..., description="Destination node ID")
    from_name: str = Field(..., description="Source node name")
    to_name: str = Field(..., description="Destination node name")
    distance: float = Field(..., description="Segment distance in meters")
    time_seconds: float = Field(..., description="Estimated walking time in seconds")


class RouteRequest(BaseModel):
    """Request for route computation."""
    start_node: int = Field(..., description="Starting node ID")
    end_node: int = Field(..., description="Ending node ID")
    algorithm: str = Field(default="dijkstra", description="Algorithm: dijkstra, floyd_warshall, bfs")
    crowd_mode: bool = Field(default=False, description="Use crowd-aware routing")
    crowd_alpha: float = Field(default=0.3, description="Crowd penalty weight (0-1)")

    class Config:
        json_schema_extra = {
            "example": {
                "start_node": 0,
                "end_node": 5,
                "algorithm": "dijkstra",
                "crowd_mode": False,
                "crowd_alpha": 0.3
            }
        }


class RouteResult(BaseModel):
    """Result of route computation."""
    path: List[int] = Field(..., description="List of node IDs in the path")
    segments: List[RouteSegment] = Field(..., description="Detailed route segments")
    total_distance: float = Field(..., description="Total distance in meters")
    total_time: float = Field(..., description="Total time in seconds")
    algorithm_used: str = Field(..., description="Algorithm used")
    computation_time_ms: float = Field(..., description="Time to compute route")
    notes: Optional[str] = Field(None, description="Additional information")

    class Config:
        json_schema_extra = {
            "example": {
                "path": [0, 3, 5],
                "segments": [
                    {
                        "from_node": 0,
                        "to_node": 3,
                        "from_name": "Main Building",
                        "to_name": "Science Block",
                        "distance": 200.0,
                        "time_seconds": 150.0
                    }
                ],
                "total_distance": 450.0,
                "total_time": 337.5,
                "algorithm_used": "dijkstra",
                "computation_time_ms": 1.2,
                "notes": None
            }
        }
