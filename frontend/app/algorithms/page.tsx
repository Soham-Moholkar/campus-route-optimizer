'use client';

export default function AlgorithmsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Algorithm Explorer</h1>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Graph Algorithms */}
        <AlgorithmCard
          title="Dijkstra's Algorithm"
          unit="Unit 5: Graph Algorithms"
          complexity="Time: O((V+E) log V), Space: O(V)"
          description="Single-source shortest path algorithm using a priority queue. Optimal for sparse graphs and single queries."
          useCase="Computing shortest walking routes between two buildings on campus."
          practical="Practical: Shortest Path Implementation"
        />

        <AlgorithmCard
          title="Floyd-Warshall"
          unit="Unit 5: Graph Algorithms"
          complexity="Time: O(V³), Space: O(V²)"
          description="All-pairs shortest paths using dynamic programming. Computes distances between every pair of nodes."
          useCase="Precomputing all distances for quick timetable evaluation."
          practical="Practical: All-Pairs Shortest Paths"
        />

        <AlgorithmCard
          title="BFS & DFS"
          unit="Unit 5: Graph Algorithms"
          complexity="Time: O(V+E), Space: O(V)"
          description="Graph traversal algorithms. BFS finds unweighted shortest paths; DFS explores deeply."
          useCase="Campus connectivity analysis and component detection."
          practical="Practical: Graph Traversal"
        />

        <AlgorithmCard
          title="Kruskal's MST"
          unit="Unit 5: Graph Algorithms (Greedy)"
          complexity="Time: O(E log V), Space: O(V)"
          description="Minimum Spanning Tree using Union-Find. Greedily selects minimum weight edges."
          useCase="Campus expansion planning - minimum cost walkway network."
          practical="Practical: MST Algorithms"
        />

        {/* Greedy Algorithms */}
        <AlgorithmCard
          title="Activity Selection"
          unit="Unit 3: Greedy Algorithms"
          complexity="Time: O(n log n), Space: O(n)"
          description="Selects maximum non-overlapping activities by earliest finish time."
          useCase="Fast timetable generation with conflict avoidance."
          practical="Practical: Job Scheduling"
        />

        {/* Dynamic Programming */}
        <AlgorithmCard
          title="Weighted Interval Scheduling"
          unit="Unit 4: Dynamic Programming"
          complexity="Time: O(n log n), Space: O(n)"
          description="Optimal selection of weighted intervals using DP. Maximizes total score."
          useCase="High-quality timetable considering student preferences."
          practical="Practical: DP Interval Problems"
        />

        <AlgorithmCard
          title="0/1 Knapsack"
          unit="Unit 4: Dynamic Programming"
          complexity="Time: O(nW), Space: O(nW)"
          description="Optimal selection under capacity constraint. Classic DP problem."
          useCase="Resource allocation variant (included for completeness)."
          practical="Practical: Knapsack Problem"
        />

        {/* Advanced Techniques */}
        <AlgorithmCard
          title="Backtracking"
          unit="Unit 6: Backtracking"
          complexity="Time: O(k^n), Space: O(n)"
          description="Exhaustive search with pruning. Explores all possibilities systematically."
          useCase="Exact scheduling for small instances (≤10 courses)."
          practical="Practical: N-Queens adapted"
        />

        <AlgorithmCard
          title="Branch & Bound"
          unit="Unit 6: Branch & Bound"
          complexity="Time: O(k^n) pruned, Space: O(n)"
          description="Optimized exhaustive search using bounds. Prunes infeasible branches."
          useCase="Optimal scheduling with walking cost optimization."
          practical="Practical: Optimization Problems"
        />

        <AlgorithmCard
          title="Parallel Processing"
          unit="Unit 6: Parallel Concepts"
          complexity="Speedup: Up to P (processors)"
          description="Multi-threaded computation for independent tasks. Demonstrates Amdahl's Law."
          useCase="Batch shortest path queries with speedup."
          practical="Practical: Parallel Algorithm Analysis"
        />
      </div>

      {/* Syllabus Mapping */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-semibold mb-4">Complete Syllabus Mapping</h2>
        <div className="space-y-4">
          <SyllabusMapping
            unit="Unit 3: Greedy Algorithms"
            topics={[
              'Activity Selection → Fast Scheduling',
              'Job Scheduling with Deadlines → Time slot allocation',
              "Kruskal's MST → Campus expansion planning",
            ]}
          />
          <SyllabusMapping
            unit="Unit 4: Dynamic Programming"
            topics={[
              'Weighted Interval Scheduling → Preference-based slots',
              '0/1 Knapsack → Resource allocation',
              'Walking cost optimization → Extended DP state',
            ]}
          />
          <SyllabusMapping
            unit="Unit 5: Graph Algorithms"
            topics={[
              'BFS/DFS → Campus connectivity',
              "Dijkstra's Algorithm → Single-source shortest paths",
              'Floyd-Warshall → All-pairs distances',
              "Kruskal's MST → Minimum spanning tree",
            ]}
          />
          <SyllabusMapping
            unit="Unit 6: Advanced Techniques"
            topics={[
              'Backtracking → Exhaustive search with pruning',
              'Branch & Bound → Optimized exact solutions',
              'Parallel algorithms → Speedup analysis',
            ]}
          />
          <SyllabusMapping
            unit="Practical 10: Sorting & Analysis"
            topics={[
              'Merge Sort vs Quick Sort benchmarks',
              'Performance analysis with plots',
              'CSV output with runtime data',
            ]}
          />
        </div>
      </div>
    </div>
  );
}

function AlgorithmCard({
  title,
  unit,
  complexity,
  description,
  useCase,
  practical,
}: {
  title: string;
  unit: string;
  complexity: string;
  description: string;
  useCase: string;
  practical: string;
}) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md space-y-3">
      <h3 className="text-xl font-semibold text-gray-900">{title}</h3>
      <div className="text-sm text-blue-600 font-medium">{unit}</div>
      <div className="text-sm bg-gray-100 px-3 py-2 rounded font-mono">{complexity}</div>
      <p className="text-gray-700 text-sm">{description}</p>
      <div className="border-t pt-3 space-y-2">
        <div className="text-sm">
          <strong className="text-gray-700">Use Case:</strong>
          <p className="text-gray-600 mt-1">{useCase}</p>
        </div>
        <div className="text-sm">
          <strong className="text-gray-700">Practical:</strong>
          <p className="text-gray-600 mt-1">{practical}</p>
        </div>
      </div>
    </div>
  );
}

function SyllabusMapping({ unit, topics }: { unit: string; topics: string[] }) {
  return (
    <div>
      <h3 className="font-semibold text-lg text-gray-900 mb-2">{unit}</h3>
      <ul className="list-disc list-inside space-y-1 text-gray-700 pl-4">
        {topics.map((topic, idx) => (
          <li key={idx} className="text-sm">
            {topic}
          </li>
        ))}
      </ul>
    </div>
  );
}
