"""
Graph service for campus graph operations and routing.
"""
from typing import Dict, List, Tuple, Optional
import random
import math
from app.models.campus import CampusGraph, Node, Edge, Room
from app.models.route import RouteRequest, RouteResult, RouteSegment
from app.algorithms.graph.dijkstra import dijkstra_path
from app.algorithms.graph.floyd_warshall import floyd_warshall_with_paths
from app.algorithms.graph.bfs_dfs import find_path_bfs
import time


class GraphService:
    """Service for graph operations."""
    
    def __init__(self):
        self.current_graph: Optional[CampusGraph] = None
        self.adjacency_list: Dict[int, List[Tuple[int, float]]] = {}
        self.floyd_cache: Optional[Dict] = None
    
    def generate_random_graph(self, num_nodes: int = 20, edge_probability: float = 0.3, 
                            seed: int = 42) -> CampusGraph:
        """
        Generate a random campus graph.
        
        Args:
            num_nodes: Number of buildings
            edge_probability: Probability of edge between nodes
            seed: Random seed
        
        Returns:
            CampusGraph instance
        """
        random.seed(seed)
        
        # Generate nodes in a grid-like pattern with some randomness
        nodes = []
        grid_size = math.ceil(math.sqrt(num_nodes))
        
        building_names = [
            "Main Building", "Library", "Science Block", "Engineering Wing",
            "Arts Building", "Admin Block", "Cafeteria", "Sports Complex",
            "Lecture Hall A", "Lecture Hall B", "Computer Center", "Research Lab",
            "Student Center", "Auditorium", "Medical Center", "Hostel A",
            "Hostel B", "Seminar Hall", "Workshop", "Innovation Hub"
        ]
        
        for i in range(num_nodes):
            row = i // grid_size
            col = i % grid_size
            x = col * 200 + random.uniform(-30, 30)
            y = row * 200 + random.uniform(-30, 30)
            name = building_names[i] if i < len(building_names) else f"Building {i}"
            nodes.append(Node(id=i, name=name, x=x, y=y))
        
        # Generate edges
        edges = []
        edge_id = 0
        
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if random.random() < edge_probability:
                    # Calculate Euclidean distance
                    dist = math.sqrt((nodes[i].x - nodes[j].x)**2 + 
                                   (nodes[i].y - nodes[j].y)**2)
                    edges.append(Edge(u=i, v=j, distance=dist, base_weight=dist))
                    edges.append(Edge(u=j, v=i, distance=dist, base_weight=dist))
        
        # Ensure connectivity (add edges to make spanning tree)
        visited = set([0])
        unvisited = set(range(1, num_nodes))
        
        while unvisited:
            # Pick random visited and unvisited nodes
            u = random.choice(list(visited))
            v = random.choice(list(unvisited))
            
            dist = math.sqrt((nodes[u].x - nodes[v].x)**2 + 
                           (nodes[u].y - nodes[v].y)**2)
            
            # Check if edge doesn't exist
            if not any(e.u == u and e.v == v for e in edges):
                edges.append(Edge(u=u, v=v, distance=dist, base_weight=dist))
                edges.append(Edge(u=v, v=u, distance=dist, base_weight=dist))
            
            visited.add(v)
            unvisited.remove(v)
        
        # Generate rooms
        rooms = []
        capacities = [30, 50, 60, 80, 100, 120, 150, 200]
        room_id = 0
        
        for node in nodes:
            num_rooms = random.randint(2, 5)
            for r in range(num_rooms):
                capacity = random.choice(capacities)
                rooms.append(Room(
                    id=room_id,
                    building_id=node.id,
                    capacity=capacity,
                    name=f"{node.name}-R{r+1}"
                ))
                room_id += 1
        
        graph = CampusGraph(nodes=nodes, edges=edges, rooms=rooms)
        self.set_graph(graph)
        
        return graph
    
    def set_graph(self, graph: CampusGraph):
        """Set the current graph and build adjacency list."""
        self.current_graph = graph
        self.adjacency_list = {}
        self.floyd_cache = None
        
        # Build adjacency list
        for edge in graph.edges:
            if edge.u not in self.adjacency_list:
                self.adjacency_list[edge.u] = []
            self.adjacency_list[edge.u].append((edge.v, edge.distance))
    
    def compute_shortest_path(self, request: RouteRequest) -> RouteResult:
        """
        Compute shortest path using specified algorithm.
        
        Args:
            request: Route request
        
        Returns:
            Route result with path and metrics
        """
        start_time = time.perf_counter()
        
        if request.algorithm == "dijkstra":
            path, distance = self._dijkstra_route(request)
        elif request.algorithm == "floyd_warshall":
            path, distance = self._floyd_warshall_route(request)
        elif request.algorithm == "bfs":
            path, distance = self._bfs_route(request)
        else:
            raise ValueError(f"Unknown algorithm: {request.algorithm}")
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        # Build segments
        segments = self._build_segments(path, distance)
        
        # Estimate walking time (assume 1.4 m/s average walking speed)
        total_time = distance / 1.4  # seconds
        
        return RouteResult(
            path=path,
            segments=segments,
            total_distance=distance,
            total_time=total_time,
            algorithm_used=request.algorithm,
            computation_time_ms=elapsed_ms,
            notes=None
        )
    
    def _dijkstra_route(self, request: RouteRequest) -> Tuple[List[int], float]:
        """Compute route using Dijkstra."""
        path, distance = dijkstra_path(self.adjacency_list, request.start_node, request.end_node)
        return path, distance
    
    def _floyd_warshall_route(self, request: RouteRequest) -> Tuple[List[int], float]:
        """Compute route using Floyd-Warshall (with caching)."""
        if self.floyd_cache is None:
            num_nodes = len(self.current_graph.nodes)
            self.floyd_cache = floyd_warshall_with_paths(self.adjacency_list, num_nodes)
        
        path, distance = self.floyd_cache["get_path"](request.start_node, request.end_node)
        return path, distance
    
    def _bfs_route(self, request: RouteRequest) -> Tuple[List[int], float]:
        """Compute route using BFS (unweighted shortest path)."""
        path = find_path_bfs(self.adjacency_list, request.start_node, request.end_node)
        
        # Compute distance along path
        distance = 0.0
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            for neighbor, weight in self.adjacency_list.get(u, []):
                if neighbor == v:
                    distance += weight
                    break
        
        return path, distance
    
    def _build_segments(self, path: List[int], total_distance: float) -> List[RouteSegment]:
        """Build route segments from path."""
        if not path or len(path) < 2:
            return []
        
        segments = []
        node_map = {node.id: node.name for node in self.current_graph.nodes}
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            
            # Find edge weight
            seg_distance = 0.0
            for neighbor, weight in self.adjacency_list.get(u, []):
                if neighbor == v:
                    seg_distance = weight
                    break
            
            seg_time = seg_distance / 1.4  # seconds
            
            segments.append(RouteSegment(
                from_node=u,
                to_node=v,
                from_name=node_map.get(u, f"Node {u}"),
                to_name=node_map.get(v, f"Node {v}"),
                distance=seg_distance,
                time_seconds=seg_time
            ))
        
        return segments
    
    def get_distance_matrix(self) -> Dict[Tuple[int, int], float]:
        """
        Get all-pairs shortest distances.
        
        Returns:
            Dict {(u, v): distance}
        """
        if self.floyd_cache is None:
            num_nodes = len(self.current_graph.nodes)
            self.floyd_cache = floyd_warshall_with_paths(self.adjacency_list, num_nodes)
        
        distance_dict = {}
        num_nodes = len(self.current_graph.nodes)
        
        for i in range(num_nodes):
            for j in range(num_nodes):
                distance_dict[(i, j)] = self.floyd_cache["distances"][i][j]
        
        return distance_dict


# Global instance
graph_service = GraphService()
