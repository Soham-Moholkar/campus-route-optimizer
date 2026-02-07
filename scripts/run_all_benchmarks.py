"""
Run all benchmark suites and generate reports.
"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.models.benchmark import BenchmarkConfig
from app.benchmarks.benchmark_runner import run_benchmark_suite


async def main():
    """Run all benchmarks."""
    print("=" * 60)
    print("SmartCampus Optimizer - Benchmark Suite")
    print("=" * 60)
    
    suites = ["sorting", "dijkstra", "schedule", "parallel"]
    
    for suite in suites:
        print(f"\n▶ Running {suite} benchmark...")
        
        config = BenchmarkConfig(
            suite=suite,
            trials=5,
            max_nodes=500,
            seed=42
        )
        
        try:
            result = await run_benchmark_suite(config)
            print(f"  ✓ Completed: {suite}")
            print(f"    CSV: {result.csv_path}")
            print(f"    Plot: {result.plot_path}")
            
            if result.summary:
                print(f"    Summary: {result.summary}")
        
        except Exception as e:
            print(f"  ✗ Failed: {suite}")
            print(f"    Error: {e}")
    
    print("\n" + "=" * 60)
    print("All benchmarks completed!")
    print("Results saved to: backend/app/benchmarks/results/")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
