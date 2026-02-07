'use client';

import React, { useState } from 'react';
import { BenchmarkResult } from '@/lib/types';
import { apiMethods } from '@/lib/api';

export default function BenchmarksPage() {
  const [result, setResult] = useState<BenchmarkResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [suite, setSuite] = useState<string>('sorting');

  const runBenchmark = async () => {
    setLoading(true);
    setError(null);
    try {
      const config = {
        suite,
        trials: 5,
        max_nodes: 500,
        seed: 42,
      };

      const benchResult = await apiMethods.runBenchmark(config);
      setResult(benchResult as BenchmarkResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to run benchmark');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Performance Benchmarks</h1>

      {/* Controls */}
      <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Benchmark Suite</label>
          <select
            value={suite}
            onChange={(e) => setSuite(e.target.value)}
            className="w-full max-w-md px-3 py-2 border rounded"
          >
            <option value="sorting">Sorting (Merge vs Quick)</option>
            <option value="dijkstra">Dijkstra Scaling</option>
            <option value="schedule">Scheduling (Greedy vs DP)</option>
            <option value="parallel">Parallel Speedup</option>
          </select>
        </div>

        <button
          onClick={runBenchmark}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Running...' : 'Run Benchmark'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Results: {result.suite}</h2>
            
            {/* Summary */}
            {result.summary && (
              <div className="mb-4 p-4 bg-gray-50 rounded">
                <h3 className="font-medium mb-2">Summary</h3>
                <pre className="text-sm">{JSON.stringify(result.summary, null, 2)}</pre>
              </div>
            )}

            {/* Data Table */}
            <div className="overflow-x-auto">
              <table className="min-w-full border-collapse border">
                <thead>
                  <tr className="bg-gray-100">
                    {result.results.length > 0 &&
                      Object.keys(result.results[0]).map((key) => (
                        <th key={key} className="border px-4 py-2 text-left">
                          {key}
                        </th>
                      ))}
                  </tr>
                </thead>
                <tbody>
                  {result.results.map((row, idx) => (
                    <tr key={idx}>
                      {Object.values(row).map((value: any, vidx) => (
                        <td key={vidx} className="border px-4 py-2">
                          {typeof value === 'number' ? value.toFixed(2) : value}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {result.csv_path && (
              <div className="mt-4 text-sm text-gray-600">
                CSV saved to: {result.csv_path}
              </div>
            )}

            {result.plot_path && (
              <div className="mt-4 text-sm text-gray-600">
                Plot saved to: {result.plot_path}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Benchmark Descriptions */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">Available Benchmarks</h2>
        <div className="space-y-4">
          <BenchmarkDescription
            title="Sorting Comparison"
            description="Compares Merge Sort and Quick Sort performance on random arrays"
            complexity="Merge Sort: O(n log n) guaranteed, Quick Sort: O(n log n) average"
          />
          <BenchmarkDescription
            title="Dijkstra Scaling"
            description="Measures Dijkstra's algorithm performance with increasing graph sizes"
            complexity="O((V+E) log V) with binary heap"
          />
          <BenchmarkDescription
            title="Scheduling Algorithms"
            description="Compares Greedy vs DP scheduling in terms of runtime and solution quality"
            complexity="Greedy: O(n log n), DP: O(n²)"
          />
          <BenchmarkDescription
            title="Parallel Speedup"
            description="Demonstrates parallel processing benefits for shortest path batch computation"
            complexity="Ideal speedup: O(n/P) where P = processors"
          />
        </div>
      </div>
    </div>
  );
}

function BenchmarkDescription({
  title,
  description,
  complexity,
}: {
  title: string;
  description: string;
  complexity: string;
}) {
  return (
    <div className="border-l-4 border-blue-600 pl-4">
      <h3 className="font-semibold text-lg">{title}</h3>
      <p className="text-gray-600 text-sm mb-1">{description}</p>
      <p className="text-sm text-gray-500">
        <strong>Complexity:</strong> {complexity}
      </p>
    </div>
  );
}
