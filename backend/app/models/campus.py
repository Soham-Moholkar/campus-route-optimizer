"""
Campus graph data models.
Represents the physical layout of the university campus.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class Node(BaseModel):
    """Represents a building or location on campus."""
    id: int = Field(..., description="Unique node identifier")
    name: str = Field(..., description="Building or location name")
    x: float = Field(..., description="X coordinate for visualization")
    y: float = Field(..., description="Y coordinate for visualization")


class Edge(BaseModel):
    """Represents a walkway between two locations."""
    u: int = Field(..., description="Source node ID")
    v: int = Field(..., description="Destination node ID")
    distance: float = Field(..., description="Walking distance in meters")
    base_weight: float = Field(..., description="Base traversal weight")


class Room(BaseModel):
    """Represents a classroom or lecture hall."""
    id: int = Field(..., description="Unique room identifier")
    building_id: int = Field(..., description="Building node ID")
    capacity: int = Field(..., description="Maximum student capacity")
    name: Optional[str] = Field(None, description="Room name/number")


class CampusGraph(BaseModel):
    """Complete campus graph structure."""
    nodes: List[Node] = Field(..., description="List of all buildings/locations")
    edges: List[Edge] = Field(..., description="List of all walkways")
    rooms: Optional[List[Room]] = Field(default_factory=list, description="Optional room list")

    class Config:
        json_schema_extra = {
            "example": {
                "nodes": [
                    {"id": 0, "name": "Main Building", "x": 0.0, "y": 0.0},
                    {"id": 1, "name": "Library", "x": 100.0, "y": 50.0}
                ],
                "edges": [
                    {"u": 0, "v": 1, "distance": 150.0, "base_weight": 150.0}
                ],
                "rooms": [
                    {"id": 0, "building_id": 0, "capacity": 50, "name": "Room 101"}
                ]
            }
        }
