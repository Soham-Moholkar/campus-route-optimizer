"""
Benchmark API endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from app.models.benchmark import BenchmarkConfig, BenchmarkResult
from app.benchmarks.benchmark_runner import run_benchmark_suite

router = APIRouter()


@router.post("/run", response_model=BenchmarkResult)
async def run_benchmark(config: BenchmarkConfig):
    """
    Run benchmark suite.
    
    Supported suites: sorting, dijkstra, schedule, parallel, all
    """
    try:
        result = await run_benchmark_suite(config)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/results")
async def list_benchmark_results():
    """List available benchmark result files."""
    try:
        results_dir = os.path.join("app", "benchmarks", "results")
        
        if not os.path.exists(results_dir):
            return {"results": []}
        
        files = []
        for filename in os.listdir(results_dir):
            if filename.endswith(('.csv', '.png')):
                files.append(filename)
        
        return {"results": files}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
