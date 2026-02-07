'use client';

import React, { useState } from 'react';
import { CampusGraph, RouteResult } from '@/lib/types';
import { apiMethods } from '@/lib/api';

export default function CampusGraphComponent() {
  const [graph, setGraph] = useState<CampusGraph | null>(null);
  const [route, setRoute] = useState<RouteResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [startNode, setStartNode] = useState<number>(0);
  const [endNode, setEndNode] = useState<number>(1);
  const [algorithm, setAlgorithm] = useState<string>('dijkstra');

  const generateGraph = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiMethods.generateGraph({
        num_nodes: 20,
        edge_probability: 0.35,
        seed: 42,
      });
      setGraph(result as CampusGraph);
      setRoute(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate graph');
    } finally {
      setLoading(false);
    }
  };

  const computeRoute = async () => {
    if (!graph) return;
    setLoading(true);
    setError(null);
    try {
      const result = await apiMethods.computeRoute({
        start_node: startNode,
        end_node: endNode,
        algorithm,
        crowd_mode: false,
      });
      setRoute(result as RouteResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to compute route');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Campus Map</h1>

      {/* Controls */}
      <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
        <button
          onClick={generateGraph}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Loading...' : 'Generate Campus Graph'}
        </button>

        {graph && (
          <div className="space-y-4">
            <div className="text-sm text-gray-600">
              Graph: {graph.nodes.length} buildings, {graph.edges.length / 2} walkways
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Start Building</label>
                <select
                  value={startNode}
                  onChange={(e) => setStartNode(Number(e.target.value))}
                  className="w-full px-3 py-2 border rounded"
                >
                  {graph.nodes.map((node) => (
                    <option key={node.id} value={node.id}>
                      {node.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">End Building</label>
                <select
                  value={endNode}
                  onChange={(e) => setEndNode(Number(e.target.value))}
                  className="w-full px-3 py-2 border rounded"
                >
                  {graph.nodes.map((node) => (
                    <option key={node.id} value={node.id}>
                      {node.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Algorithm</label>
                <select
                  value={algorithm}
                  onChange={(e) => setAlgorithm(e.target.value)}
                  className="w-full px-3 py-2 border rounded"
                >
                  <option value="dijkstra">Dijkstra</option>
                  <option value="floyd_warshall">Floyd-Warshall</option>
                  <option value="bfs">BFS</option>
                </select>
              </div>
            </div>

            <button
              onClick={computeRoute}
              disabled={loading}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50"
            >
              Compute Shortest Path
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Route Result */}
      {route && (
        <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
          <h2 className="text-xl font-semibold">Route Details</h2>
          
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span className="font-medium">Distance:</span> {route.total_distance.toFixed(2)}m
            </div>
            <div>
              <span className="font-medium">Time:</span> {(route.total_time / 60).toFixed(1)} min
            </div>
            <div>
              <span className="font-medium">Algorithm:</span> {route.algorithm_used}
            </div>
          </div>

          <div>
            <h3 className="font-medium mb-2">Path:</h3>
            <div className="space-y-2">
              {route.segments.map((seg, idx) => (
                <div key={idx} className="flex items-center text-sm">
                  <span className="text-blue-600">→</span>
                  <span className="ml-2">{seg.from_name}</span>
                  <span className="mx-2 text-gray-400">to</span>
                  <span>{seg.to_name}</span>
                  <span className="ml-auto text-gray-500">
                    {seg.distance.toFixed(0)}m ({(seg.time_seconds / 60).toFixed(1)} min)
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="text-xs text-gray-500">
            Computed in {route.computation_time_ms.toFixed(2)}ms
          </div>
        </div>
      )}

      {/* Simple Graph Visualization */}
      {graph && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Graph Visualization</h2>
          <div className="relative bg-gray-50 rounded" style={{ height: '500px' }}>
            <svg width="100%" height="100%" viewBox="0 0 1000 800">
              {/* Draw edges */}
              {graph.edges.map((edge, idx) => {
                const fromNode = graph.nodes.find((n) => n.id === edge.u);
                const toNode = graph.nodes.find((n) => n.id === edge.v);
                if (!fromNode || !toNode) return null;

                const isInPath = route && route.path.includes(edge.u) && route.path.includes(edge.v) &&
                  Math.abs(route.path.indexOf(edge.u) - route.path.indexOf(edge.v)) === 1;

                return (
                  <line
                    key={idx}
                    x1={fromNode.x + 100}
                    y1={fromNode.y + 100}
                    x2={toNode.x + 100}
                    y2={toNode.y + 100}
                    stroke={isInPath ? '#3b82f6' : '#d1d5db'}
                    strokeWidth={isInPath ? 3 : 1}
                  />
                );
              })}

              {/* Draw nodes */}
              {graph.nodes.map((node) => {
                const isInPath = route && route.path.includes(node.id);
                const isStart = node.id === startNode;
                const isEnd = node.id === endNode;

                return (
                  <g key={node.id}>
                    <circle
                      cx={node.x + 100}
                      cy={node.y + 100}
                      r={isStart || isEnd ? 8 : 6}
                      fill={isStart ? '#10b981' : isEnd ? '#ef4444' : isInPath ? '#3b82f6' : '#6b7280'}
                    />
                    <text
                      x={node.x + 100}
                      y={node.y + 85}
                      textAnchor="middle"
                      fontSize="10"
                      fill="#374151"
                    >
                      {node.name.length > 15 ? node.name.slice(0, 12) + '...' : node.name}
                    </text>
                  </g>
                );
              })}
            </svg>
          </div>
          <div className="mt-2 text-sm text-gray-600">
            <span className="inline-block w-3 h-3 bg-green-600 rounded-full mr-1"></span> Start
            <span className="inline-block w-3 h-3 bg-red-600 rounded-full ml-4 mr-1"></span> End
            <span className="inline-block w-3 h-3 bg-blue-600 rounded-full ml-4 mr-1"></span> Path
          </div>
        </div>
      )}
    </div>
  );
}
