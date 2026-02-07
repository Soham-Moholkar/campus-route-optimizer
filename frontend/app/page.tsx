'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-4 text-gray-900">
          SmartCampus Path + Slot Optimizer
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Campus-scale optimization engine using classical DAA algorithms
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/campus-map"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Campus Map
          </Link>
          <Link
            href="/timetable"
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Generate Timetable
          </Link>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-2 gap-6 mb-12">
        <FeatureCard
          title="Conflict-Free Scheduling"
          description="Generate timetables with no overlapping time slots using Greedy, DP, and Branch & Bound algorithms"
          icon="📅"
        />
        <FeatureCard
          title="Shortest Path Routing"
          description="Compute optimal routes between classes using Dijkstra, Floyd-Warshall, and crowd-aware algorithms"
          icon="🗺️"
        />
        <FeatureCard
          title="Performance Benchmarks"
          description="Comprehensive performance analysis with runtime comparisons and visualization"
          icon="📊"
        />
        <FeatureCard
          title="Algorithm Explorer"
          description="Learn about algorithms with complexity analysis and syllabus mapping"
          icon="🧠"
        />
      </div>

      {/* Algorithm Overview */}
      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-bold mb-6 text-gray-900">Implemented Algorithms</h2>
        
        <div className="space-y-4">
          <AlgorithmSection
            title="Graph Algorithms (Unit 5)"
            algorithms={[
              "Dijkstra's Algorithm - O((V+E) log V)",
              "Floyd-Warshall - O(V³)",
              "BFS/DFS - O(V+E)",
              "Kruskal's MST - O(E log V)"
            ]}
          />
          
          <AlgorithmSection
            title="Greedy Algorithms (Unit 3)"
            algorithms={[
              "Activity Selection - O(n log n)",
              "Job Scheduling with Deadlines"
            ]}
          />
          
          <AlgorithmSection
            title="Dynamic Programming (Unit 4)"
            algorithms={[
              "Weighted Interval Scheduling - O(n log n)",
              "0/1 Knapsack - O(nW)"
            ]}
          />
          
          <AlgorithmSection
            title="Advanced Techniques (Unit 6)"
            algorithms={[
              "Backtracking - O(k^n)",
              "Branch & Bound with pruning",
              "Parallel Path Computation"
            ]}
          />
        </div>
      </div>

      {/* Quick Links */}
      <div className="mt-12 grid md:grid-cols-4 gap-4">
        <QuickLink href="/campus-map" title="Campus Map" />
        <QuickLink href="/timetable" title="Timetable" />
        <QuickLink href="/benchmarks" title="Benchmarks" />
        <QuickLink href="/algorithms" title="Algorithms" />
      </div>
    </div>
  );
}

function FeatureCard({ title, description, icon }: { title: string; description: string; icon: string }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="text-xl font-semibold mb-2 text-gray-900">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}

function AlgorithmSection({ title, algorithms }: { title: string; algorithms: string[] }) {
  return (
    <div>
      <h3 className="text-lg font-semibold mb-2 text-gray-800">{title}</h3>
      <ul className="list-disc list-inside space-y-1 text-gray-600 pl-4">
        {algorithms.map((algo, idx) => (
          <li key={idx}>{algo}</li>
        ))}
      </ul>
    </div>
  );
}

function QuickLink({ href, title }: { href: string; title: string }) {
  return (
    <Link
      href={href}
      className="block p-4 bg-gray-100 rounded-lg text-center hover:bg-gray-200 transition-colors"
    >
      <span className="font-medium text-gray-900">{title}</span>
    </Link>
  );
}
