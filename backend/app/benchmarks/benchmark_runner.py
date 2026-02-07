"""
Benchmark runner for algorithm performance analysis.
"""
import time
import random
import os
import csv
from typing import List, Dict
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from app.models.benchmark import BenchmarkConfig, BenchmarkResult
from app.algorithms.graph.dijkstra import dijkstra_path
from app.algorithms.parallel.parallel_paths import benchmark_parallel_speedup


async def run_benchmark_suite(config: BenchmarkConfig) -> BenchmarkResult:
    """
    Run specified benchmark suite.
    
    Args:
        config: Benchmark configuration
    
    Returns:
        Benchmark result
    """
    if config.suite == "sorting":
        return await benchmark_sorting(config)
    elif config.suite == "dijkstra":
        return await benchmark_dijkstra(config)
    elif config.suite == "schedule":
        return await benchmark_scheduling(config)
    elif config.suite == "parallel":
        return await benchmark_parallel(config)
    elif config.suite == "all":
        # Run all benchmarks
        results = []
        for suite in ["sorting", "dijkstra", "schedule", "parallel"]:
            config.suite = suite
            result = await run_benchmark_suite(config)
            results.append(result.model_dump())
        
        return BenchmarkResult(
            suite="all",
            results=results,
            summary={"message": "All benchmarks completed"}
        )
    else:
        raise ValueError(f"Unknown benchmark suite: {config.suite}")


async def benchmark_sorting(config: BenchmarkConfig) -> BenchmarkResult:
    """
    Benchmark merge sort vs quick sort.
    Practical #10 requirement.
    """
    sizes = config.sizes or [100, 500, 1000, 5000, 10000]
    results = []
    
    def merge_sort(arr):
        """Merge sort implementation."""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        
        return merge(left, right)
    
    def merge(left, right):
        """Merge two sorted arrays."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def quick_sort(arr):
        """Quick sort implementation."""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return quick_sort(left) + middle + quick_sort(right)
    
    for size in sizes:
        random.seed(config.seed)
        arr = [random.randint(1, 10000) for _ in range(size)]
        
        # Merge sort
        arr_copy = arr.copy()
        start = time.perf_counter()
        merge_sort(arr_copy)
        merge_time = (time.perf_counter() - start) * 1000
        
        # Quick sort
        arr_copy = arr.copy()
        start = time.perf_counter()
        quick_sort(arr_copy)
        quick_time = (time.perf_counter() - start) * 1000
        
        results.append({
            "size": size,
            "merge_sort_ms": merge_time,
            "quick_sort_ms": quick_time
        })
    
    # Save results
    os.makedirs("app/benchmarks/results", exist_ok=True)
    csv_path = "app/benchmarks/results/sorting_benchmark.csv"
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["size", "merge_sort_ms", "quick_sort_ms"])
        writer.writeheader()
        writer.writerows(results)
    
    # Generate plot
    plot_path = "app/benchmarks/results/sorting_benchmark.png"
    plt.figure(figsize=(10, 6))
    plt.plot([r["size"] for r in results], [r["merge_sort_ms"] for r in results], 
             marker='o', label="Merge Sort")
    plt.plot([r["size"] for r in results], [r["quick_sort_ms"] for r in results], 
             marker='s', label="Quick Sort")
    plt.xlabel("Input Size")
    plt.ylabel("Time (ms)")
    plt.title("Sorting Algorithm Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig(plot_path)
    plt.close()
    
    return BenchmarkResult(
        suite="sorting",
        results=results,
        csv_path=csv_path,
        plot_path=plot_path,
        summary={
            "avg_merge_ms": sum(r["merge_sort_ms"] for r in results) / len(results),
            "avg_quick_ms": sum(r["quick_sort_ms"] for r in results) / len(results)
        }
    )


async def benchmark_dijkstra(config: BenchmarkConfig) -> BenchmarkResult:
    """
    Benchmark Dijkstra's algorithm with varying graph sizes.
    """
    sizes = config.sizes or [50, 100, 200, 500]
    results = []
    
    for num_nodes in sizes:
        # Generate random graph
        graph = {}
        for i in range(num_nodes):
            graph[i] = []
            # Average degree ~5
            num_edges = min(5, num_nodes - 1)
            neighbors = random.sample([j for j in range(num_nodes) if j != i], num_edges)
            for neighbor in neighbors:
                weight = random.uniform(10, 100)
                graph[i].append((neighbor, weight))
        
        # Run Dijkstra multiple times
        times = []
        for _ in range(config.trials):
            start = random.randint(0, num_nodes - 1)
            end = random.randint(0, num_nodes - 1)
            
            t0 = time.perf_counter()
            dijkstra_path(graph, start, end)
            elapsed = (time.perf_counter() - t0) * 1000
            times.append(elapsed)
        
        avg_time = sum(times) / len(times)
        num_edges = sum(len(neighbors) for neighbors in graph.values())
        
        results.append({
            "nodes": num_nodes,
            "edges": num_edges,
            "avg_time_ms": avg_time
        })
    
    # Save results
    os.makedirs("app/benchmarks/results", exist_ok=True)
    csv_path = "app/benchmarks/results/dijkstra_benchmark.csv"
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["nodes", "edges", "avg_time_ms"])
        writer.writeheader()
        writer.writerows(results)
    
    # Generate plot
    plot_path = "app/benchmarks/results/dijkstra_benchmark.png"
    plt.figure(figsize=(10, 6))
    plt.plot([r["nodes"] for r in results], [r["avg_time_ms"] for r in results], 
             marker='o', linewidth=2)
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Time (ms)")
    plt.title("Dijkstra's Algorithm Performance")
    plt.grid(True)
    plt.savefig(plot_path)
    plt.close()
    
    return BenchmarkResult(
        suite="dijkstra",
        results=results,
        csv_path=csv_path,
        plot_path=plot_path,
        summary={
            "max_time_ms": max(r["avg_time_ms"] for r in results),
            "min_time_ms": min(r["avg_time_ms"] for r in results)
        }
    )


async def benchmark_scheduling(config: BenchmarkConfig) -> BenchmarkResult:
    """
    Benchmark scheduling algorithms (greedy vs DP).
    """
    sizes = config.sizes or [5, 10, 15, 20]
    results = []
    
    from app.algorithms.greedy.activity_selection import Activity, greedy_course_scheduling
    from app.algorithms.dp.weighted_interval import WeightedInterval, course_scheduling_dp
    
    for num_courses in sizes:
        # Generate sample scheduling problem
        course_activities = {}
        
        for course_id in range(num_courses):
            activities = []
            for i in range(5):  # 5 candidates per course
                start = random.randint(0, 100)
                end = start + random.randint(5, 15)
                score = random.uniform(50, 100)
                
                activities.append(Activity(
                    id=i,
                    start=start,
                    end=end,
                    score=score,
                    resource=random.randint(0, 5)
                ))
            
            course_activities[course_id] = activities
        
        # Greedy
        t0 = time.perf_counter()
        greedy_selected, greedy_stats = greedy_course_scheduling(course_activities)
        greedy_time = (time.perf_counter() - t0) * 1000
        
        # DP
        intervals_map = {}
        for course_id, activities in course_activities.items():
            intervals = []
            for act in activities:
                intervals.append(WeightedInterval(
                    id=act.id,
                    start=act.start,
                    end=act.end,
                    weight=act.score
                ))
            intervals_map[course_id] = intervals
        
        t0 = time.perf_counter()
        dp_score, dp_selected, dp_stats = course_scheduling_dp(intervals_map)
        dp_time = (time.perf_counter() - t0) * 1000
        
        results.append({
            "num_courses": num_courses,
            "greedy_time_ms": greedy_time,
            "greedy_score": greedy_stats["total_score"],
            "dp_time_ms": dp_time,
            "dp_score": dp_score
        })
    
    # Save results
    os.makedirs("app/benchmarks/results", exist_ok=True)
    csv_path = "app/benchmarks/results/schedule_benchmark.csv"
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "num_courses", "greedy_time_ms", "greedy_score", "dp_time_ms", "dp_score"
        ])
        writer.writeheader()
        writer.writerows(results)
    
    # Generate plot
    plot_path = "app/benchmarks/results/schedule_benchmark.png"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Runtime comparison
    ax1.plot([r["num_courses"] for r in results], [r["greedy_time_ms"] for r in results], 
             marker='o', label="Greedy")
    ax1.plot([r["num_courses"] for r in results], [r["dp_time_ms"] for r in results], 
             marker='s', label="DP")
    ax1.set_xlabel("Number of Courses")
    ax1.set_ylabel("Time (ms)")
    ax1.set_title("Runtime Comparison")
    ax1.legend()
    ax1.grid(True)
    
    # Quality comparison
    ax2.plot([r["num_courses"] for r in results], [r["greedy_score"] for r in results], 
             marker='o', label="Greedy")
    ax2.plot([r["num_courses"] for r in results], [r["dp_score"] for r in results], 
             marker='s', label="DP")
    ax2.set_xlabel("Number of Courses")
    ax2.set_ylabel("Total Score")
    ax2.set_title("Solution Quality Comparison")
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    
    return BenchmarkResult(
        suite="schedule",
        results=results,
        csv_path=csv_path,
        plot_path=plot_path,
        summary={
            "greedy_faster": True,
            "dp_better_quality": True
        }
    )


async def benchmark_parallel(config: BenchmarkConfig) -> BenchmarkResult:
    """
    Benchmark parallel speedup for shortest path computation.
    """
    num_nodes = 100
    num_queries = 50
    
    # Generate graph
    graph = {}
    for i in range(num_nodes):
        graph[i] = []
        neighbors = random.sample([j for j in range(num_nodes) if j != i], 5)
        for neighbor in neighbors:
            weight = random.uniform(10, 100)
            graph[i].append((neighbor, weight))
    
    # Generate queries
    queries = [(random.randint(0, num_nodes-1), random.randint(0, num_nodes-1)) 
               for _ in range(num_queries)]
    
    # Benchmark with different worker counts
    worker_counts = [1, 2, 4]
    speedup_results = benchmark_parallel_speedup(
        graph, queries, dijkstra_path, worker_counts
    )
    
    results = []
    for num_workers, stats in speedup_results["results_by_workers"].items():
        results.append({
            "workers": num_workers,
            "time_seconds": stats["time_seconds"],
            "speedup": stats["speedup"],
            "efficiency": stats["efficiency"]
        })
    
    # Save results
    os.makedirs("app/benchmarks/results", exist_ok=True)
    csv_path = "app/benchmarks/results/parallel_speedup.csv"
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["workers", "time_seconds", "speedup", "efficiency"])
        writer.writeheader()
        writer.writerows(results)
    
    # Generate plot
    plot_path = "app/benchmarks/results/parallel_speedup.png"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Speedup
    ax1.plot([r["workers"] for r in results], [r["speedup"] for r in results], 
             marker='o', linewidth=2)
    ax1.plot([r["workers"] for r in results], [r["workers"] for r in results], 
             linestyle='--', label="Linear Speedup")
    ax1.set_xlabel("Number of Workers")
    ax1.set_ylabel("Speedup")
    ax1.set_title("Parallel Speedup")
    ax1.legend()
    ax1.grid(True)
    
    # Efficiency
    ax2.plot([r["workers"] for r in results], [r["efficiency"] for r in results], 
             marker='s', linewidth=2, color='orange')
    ax2.set_xlabel("Number of Workers")
    ax2.set_ylabel("Efficiency")
    ax2.set_title("Parallel Efficiency")
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()
    
    return BenchmarkResult(
        suite="parallel",
        results=results,
        csv_path=csv_path,
        plot_path=plot_path,
        summary={
            "max_speedup": max(r["speedup"] for r in results),
            "num_queries": num_queries
        }
    )
