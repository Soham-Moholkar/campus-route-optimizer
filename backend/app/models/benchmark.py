"""
Benchmark data models.
Represents benchmark configurations and results.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class BenchmarkConfig(BaseModel):
    """Configuration for benchmark runs."""
    suite: str = Field(..., description="Benchmark suite: sorting, dijkstra, schedule, parallel, all")
    sizes: Optional[List[int]] = Field(default=None, description="Input sizes to test")
    trials: int = Field(default=5, description="Number of trials per size")
    max_nodes: Optional[int] = Field(default=200, description="Max nodes for graph benchmarks")
    seed: int = Field(default=42, description="Random seed for reproducibility")

    class Config:
        json_schema_extra = {
            "example": {
                "suite": "dijkstra",
                "sizes": [50, 100, 200, 500],
                "trials": 5,
                "max_nodes": 500,
                "seed": 42
            }
        }


class BenchmarkResult(BaseModel):
    """Result of a benchmark run."""
    suite: str = Field(..., description="Benchmark suite name")
    results: List[Dict] = Field(..., description="Raw benchmark data")
    csv_path: Optional[str] = Field(None, description="Path to CSV output")
    plot_path: Optional[str] = Field(None, description="Path to plot image")
    summary: Dict = Field(..., description="Summary statistics")

    class Config:
        json_schema_extra = {
            "example": {
                "suite": "dijkstra",
                "results": [
                    {"nodes": 50, "edges": 120, "time_ms": 0.5},
                    {"nodes": 100, "edges": 250, "time_ms": 1.2}
                ],
                "csv_path": "results/dijkstra_benchmark.csv",
                "plot_path": "results/dijkstra_benchmark.png",
                "summary": {
                    "avg_time_ms": 0.85,
                    "max_time_ms": 1.2
                }
            }
        }
