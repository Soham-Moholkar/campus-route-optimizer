"""
Parallel Shortest Path Computation.
Unit 6: Parallel Algorithms Concept

Demonstrates parallelization of independent shortest path queries.
Measures speedup and efficiency.

Time Complexity: O((V+E) log V / P) ideal speedup with P processors
Actual speedup limited by Amdahl's Law and overhead.
"""
from typing import List, Dict, Tuple, Callable
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time


def parallel_shortest_paths_batch(graph: Dict[int, List[Tuple[int, float]]], 
                                  queries: List[Tuple[int, int]],
                                  path_func: Callable,
                                  max_workers: int = 4,
                                  use_processes: bool = False) -> List[Tuple[List[int], float, float]]:
    """
    Compute multiple shortest paths in parallel.
    
    Args:
        graph: Adjacency list
        queries: List of (start, end) tuples
        path_func: Function to compute single path (e.g., dijkstra_path)
        max_workers: Number of parallel workers
        use_processes: Use ProcessPoolExecutor instead of ThreadPoolExecutor
    
    Returns:
        List of (path, distance, time_ms) tuples
    """
    def compute_single(query: Tuple[int, int]) -> Tuple[List[int], float, float]:
        """Compute single path with timing."""
        start_time = time.perf_counter()
        start_node, end_node = query
        path, distance = path_func(graph, start_node, end_node)
        elapsed = (time.perf_counter() - start_time) * 1000  # ms
        return (path, distance, elapsed)
    
    results = []
    
    ExecutorClass = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
    
    with ExecutorClass(max_workers=max_workers) as executor:
        future_to_query = {executor.submit(compute_single, query): query for query in queries}
        
        for future in as_completed(future_to_query):
            result = future.result()
            results.append(result)
    
    return results


def benchmark_parallel_speedup(graph: Dict[int, List[Tuple[int, float]]], 
                               queries: List[Tuple[int, int]],
                               path_func: Callable,
                               max_workers_list: List[int] = [1, 2, 4, 8]) -> Dict:
    """
    Benchmark parallel speedup with varying number of workers.
    
    Args:
        graph: Adjacency list
        queries: List of path queries
        path_func: Shortest path function
        max_workers_list: List of worker counts to test
    
    Returns:
        Dict with timing results and speedup metrics
    """
    results = {}
    baseline_time = None
    
    for num_workers in max_workers_list:
        start_time = time.perf_counter()
        
        if num_workers == 1:
            # Sequential execution
            paths = []
            for start, end in queries:
                path, dist = path_func(graph, start, end)
                paths.append((path, dist, 0.0))
        else:
            # Parallel execution
            paths = parallel_shortest_paths_batch(
                graph, queries, path_func, 
                max_workers=num_workers, 
                use_processes=False
            )
        
        elapsed = time.perf_counter() - start_time
        
        if num_workers == 1:
            baseline_time = elapsed
        
        speedup = baseline_time / elapsed if baseline_time else 1.0
        efficiency = speedup / num_workers
        
        results[num_workers] = {
            "time_seconds": elapsed,
            "speedup": speedup,
            "efficiency": efficiency,
            "paths_computed": len(paths)
        }
    
    return {
        "results_by_workers": results,
        "baseline_time": baseline_time,
        "num_queries": len(queries)
    }


def parallel_dijkstra_multi_source(graph: Dict[int, List[Tuple[int, float]]], 
                                   sources: List[int],
                                   dijkstra_func: Callable,
                                   max_workers: int = 4) -> Dict[int, Dict]:
    """
    Run Dijkstra from multiple sources in parallel.
    
    Useful for precomputing distances from multiple important locations.
    
    Args:
        graph: Adjacency list
        sources: List of source nodes
        dijkstra_func: Dijkstra function that returns {distances, parent}
        max_workers: Number of parallel workers
    
    Returns:
        Dict {source: dijkstra_result}
    """
    def compute_from_source(source: int) -> Tuple[int, Dict]:
        """Compute Dijkstra from single source."""
        result = dijkstra_func(graph, source)
        return (source, result)
    
    results_map = {}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_source = {executor.submit(compute_from_source, src): src for src in sources}
        
        for future in as_completed(future_to_source):
            source, result = future.result()
            results_map[source] = result
    
    return results_map


def parallel_schedule_evaluation(candidate_schedules: List[Dict], 
                                 evaluation_func: Callable,
                                 max_workers: int = 4) -> List[Tuple[Dict, float]]:
    """
    Evaluate multiple candidate schedules in parallel.
    
    Args:
        candidate_schedules: List of schedule dictionaries
        evaluation_func: Function that scores a schedule
        max_workers: Number of parallel workers
    
    Returns:
        List of (schedule, score) tuples sorted by score
    """
    def evaluate_single(schedule: Dict) -> Tuple[Dict, float]:
        """Evaluate single schedule."""
        score = evaluation_func(schedule)
        return (schedule, score)
    
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_schedule = {executor.submit(evaluate_single, sched): sched 
                             for sched in candidate_schedules}
        
        for future in as_completed(future_to_schedule):
            result = future.result()
            results.append(result)
    
    # Sort by score (descending)
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results


def amdahls_law_estimate(parallel_fraction: float, num_processors: int) -> float:
    """
    Estimate speedup using Amdahl's Law.
    
    Speedup = 1 / ((1 - P) + P/N)
    where P = parallel fraction, N = number of processors
    
    Args:
        parallel_fraction: Fraction of work that can be parallelized (0-1)
        num_processors: Number of processors
    
    Returns:
        Theoretical speedup
    """
    if parallel_fraction < 0 or parallel_fraction > 1:
        raise ValueError("parallel_fraction must be between 0 and 1")
    
    serial_fraction = 1 - parallel_fraction
    speedup = 1 / (serial_fraction + parallel_fraction / num_processors)
    
    return speedup


def gustafson_law_estimate(parallel_fraction: float, num_processors: int) -> float:
    """
    Estimate speedup using Gustafson's Law (scaled speedup).
    
    Speedup = (1 - P) + P * N
    where P = parallel fraction, N = number of processors
    
    Args:
        parallel_fraction: Fraction of parallel work (0-1)
        num_processors: Number of processors
    
    Returns:
        Scaled speedup
    """
    if parallel_fraction < 0 or parallel_fraction > 1:
        raise ValueError("parallel_fraction must be between 0 and 1")
    
    serial_fraction = 1 - parallel_fraction
    speedup = serial_fraction + parallel_fraction * num_processors
    
    return speedup
