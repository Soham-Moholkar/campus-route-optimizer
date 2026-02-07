# SmartCampus Path + Slot Optimizer

A campus-scale optimization engine that generates conflict-free timetables and walking routes between classes using classical DAA algorithms.

## 🎯 Problem Statement

University students face two interconnected scheduling challenges:
1. **Timetable Conflicts**: Choosing course slots without overlaps while respecting room capacities
2. **Walking Distance**: Minimizing campus traversal time between consecutive classes

This project implements a comprehensive solution using fundamental algorithms from Design and Analysis of Algorithms (DAA).

## ✨ Features

### Core Optimization
- **Conflict-Free Scheduling**: Generate timetables with no overlapping time slots
- **Room Capacity Constraints**: Ensure adequate classroom capacity
- **Walking Distance Minimization**: Optimize routes between consecutive classes
- **Multiple Solving Modes**:
  - **Fast Mode**: Greedy algorithm (O(n log n))
  - **DP Mode**: Weighted interval scheduling (O(n²))
  - **Exact Mode**: Branch & Bound for optimal solutions (≤10 courses)

### Routing Algorithms
- **Dijkstra's Algorithm**: Single-source shortest paths (O((V+E) log V))
- **Floyd-Warshall**: All-pairs shortest paths (O(V³))
- **BFS/DFS**: Graph traversal and connectivity
- **Kruskal's MST**: Campus expansion planning (O(E log V))

### Advanced Features
- **Crowd-Aware Routing**: Dynamic edge weights based on congestion simulation
- **Parallel Processing**: Multi-threaded path computation with speedup analysis
- **Comprehensive Benchmarking**: Performance analysis with visualization

### Interactive UI
- Campus map visualization with route highlighting
- Interactive timetable optimizer
- Real-time benchmark execution and charting
- Algorithm explorer with complexity analysis

## 🏗️ Tech Stack

### Backend
- **Python 3.11+**: Core language
- **FastAPI**: REST API framework
- **Pydantic**: Data validation
- **NetworkX**: Graph utilities (core algorithms implemented manually)
- **Matplotlib**: Benchmark visualization
- **Pytest**: Unit testing

### Frontend
- **Next.js 14**: React framework (App Router)
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **shadcn/ui**: UI components

## 📋 Prerequisites

- **Python 3.11+**
- **Node.js 18+** and npm
- **Git**

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd smartcampus-optimizer
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 3. Start Backend Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- OpenAPI docs: `http://localhost:8000/docs`

### 4. Frontend Setup (New Terminal)

```bash
cd frontend
npm install
```

### 5. Start Frontend

```bash
npm run dev
```

The UI will be available at `http://localhost:3000`

## 📱 Demo Walkthrough

### Step 1: Generate Campus Data

```bash
cd scripts
python generate_sample_data.py
```

This creates a sample campus graph with 20 buildings and 40+ courses.

### Step 2: Explore Campus Map

1. Navigate to **Campus Map** page
2. Select start and end buildings
3. Choose routing algorithm (Dijkstra/Floyd-Warshall/Crowd-Aware)
4. View highlighted shortest path with distance metrics

### Step 3: Generate Timetable

1. Go to **Timetable Optimizer** page
2. Select number of courses (4-8 for demo)
3. Choose optimization mode:
   - **Fast**: Greedy (instant results)
   - **DP**: Better quality (1-2 seconds)
   - **Exact**: Optimal (only for ≤10 courses)
4. View generated schedule with walking routes

### Step 4: Run Benchmarks

1. Visit **Benchmarks** page
2. Click "Run Benchmark Suite"
3. View performance charts:
   - Runtime vs input size
   - Algorithm comparison
   - Parallel speedup

### Step 5: Learn Algorithms

1. Go to **Algorithm Explorer**
2. Browse algorithm cards with:
   - Description
   - Time/space complexity
   - Syllabus mapping

## 🎓 Algorithm Mapping to DAA Syllabus

### Unit 3: Greedy Algorithms
- **Activity Selection** → Fast timetable scheduling
- **Kruskal's MST** → Campus expansion planning
- **Practical**: Job Scheduling (adapted to course slots)

### Unit 4: Dynamic Programming
- **Weighted Interval Scheduling** → Preference-based slot selection
- **Complexity**: O(n²) with walking cost optimization
- **Practical**: 0/1 Knapsack variant (resource allocation)

### Unit 5: Graph Algorithms
- **BFS/DFS** → Campus connectivity analysis
- **Dijkstra** → Single-source shortest paths (O((V+E) log V))
- **Floyd-Warshall** → All-pairs distances (O(V³))
- **Kruskal's MST** → Minimum spanning tree (O(E log V))
- **Practical**: Graph traversal + shortest path implementations

### Unit 6: Advanced Techniques
- **Backtracking** → Exhaustive schedule search with pruning
- **Branch & Bound** → Optimal scheduling with bounds
- **Parallelization** → Multi-threaded path computation
- **Practical**: N-Queens adapted to slot assignment

### Practical 10: Sorting & Analysis
- **Merge Sort vs Quick Sort** → Using roll numbers/random data
- **Performance Benchmarking** → CSV output + matplotlib plots

## 📊 Complexity Analysis

| Algorithm | Time Complexity | Space Complexity | Use Case |
|-----------|----------------|------------------|----------|
| Dijkstra | O((V+E) log V) | O(V) | Single-source shortest path |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest paths |
| BFS | O(V+E) | O(V) | Graph traversal |
| DFS | O(V+E) | O(V) | Connectivity check |
| Kruskal's MST | O(E log V) | O(V) | Minimum spanning tree |
| Greedy Schedule | O(n log n) | O(n) | Fast feasible solution |
| DP Schedule | O(n²) | O(n) | Optimal with constraints |
| Backtracking | O(k^n) worst | O(n) | Exact small instances |
| Branch & Bound | O(k^n) pruned | O(n) | Optimized exact search |

## 🔬 Benchmarking

### Run All Benchmarks

```bash
cd scripts
python run_all_benchmarks.py
```

Results saved to `backend/app/benchmarks/results/`:
- `sorting_benchmark.csv`
- `dijkstra_benchmark.csv`
- `schedule_benchmark.csv`
- `parallel_speedup.csv`
- Corresponding PNG plots

### Manual Benchmark via API

```bash
curl -X POST "http://localhost:8000/bench/run" \
  -H "Content-Type: application/json" \
  -d '{"suite": "dijkstra", "max_nodes": 500, "trials": 5}'
```

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

Test coverage includes:
- Dijkstra correctness on known graphs
- Floyd-Warshall all-pairs distances
- DP weighted interval scheduling
- Constraint validation

## 📡 API Reference

### Health Check
```
GET /health
```

### Generate Campus Graph
```
POST /generate/campus_graph
Body: {"num_nodes": 20, "edge_probability": 0.3, "seed": 42}
```

### Shortest Path
```
POST /route/shortest
Body: {
  "start_node": 0,
  "end_node": 5,
  "algorithm": "dijkstra",  // or "floyd_warshall"
  "crowd_mode": false
}
```

### Schedule Generation
```
POST /schedule/fast        // Greedy
POST /schedule/dp          // Dynamic Programming
POST /schedule/exact       // Branch & Bound
Body: {
  "num_courses": 6,
  "constraints": {
    "max_walking_distance": 1000,
    "max_idle_minutes": 60
  }
}
```

### Crowd Simulation
```
POST /crowd/simulate
Body: {"flow_intensity": 0.5, "time_window": "peak"}
```

### Run Benchmarks
```
POST /bench/run
Body: {"suite": "all", "trials": 10}
```

See full OpenAPI spec at `http://localhost:8000/docs`

## 🛠️ Project Structure

```
smartcampus-optimizer/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app entry
│   │   ├── models/                    # Pydantic schemas
│   │   ├── algorithms/                # Core algorithms
│   │   │   ├── graph/                # Graph algorithms
│   │   │   ├── greedy/               # Greedy strategies
│   │   │   ├── dp/                   # Dynamic programming
│   │   │   ├── exact/                # Backtracking & B&B
│   │   │   └── parallel/             # Parallel implementations
│   │   ├── services/                 # Business logic
│   │   ├── api/                      # Route handlers
│   │   ├── benchmarks/               # Benchmark utilities
│   │   └── data/                     # Sample datasets
│   └── tests/                        # Unit tests
├── frontend/
│   ├── app/                          # Next.js pages
│   ├── components/                   # React components
│   └── lib/                          # API client & types
├── scripts/                          # Utilities
└── report/                           # Documentation
```

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Instant feedback on optimization
- **Error Handling**: Graceful degradation with user-friendly messages
- **Accessibility**: ARIA labels and keyboard navigation
- **Dark Mode Ready**: Tailwind dark mode support

## 🔧 Configuration

### Backend Config

Edit `backend/app/main.py` for:
- CORS origins
- API rate limits
- Default graph size

### Frontend Config

Edit `frontend/lib/api.ts` for:
- API base URL
- Request timeouts
- Retry logic

## 📈 Performance Benchmarks (Sample Results)

### Dijkstra Scaling
- 50 nodes: ~0.5ms
- 100 nodes: ~1.2ms
- 500 nodes: ~8ms

### Scheduling Algorithms
- Greedy (50 courses): ~5ms
- DP (50 courses): ~120ms
- Exact (10 courses): ~300ms

### Parallel Speedup
- 4 cores: 3.2x speedup (shortest path batch)
- 8 cores: 5.8x speedup

## ⚠️ Limitations

1. **Exact Mode**: Feasible only for ≤12 courses (exponential complexity)
2. **Floyd-Warshall**: Memory intensive for graphs >1000 nodes
3. **Crowd Simulation**: Simplified model (not using real-time data)
4. **Frontend Rendering**: Canvas performance degrades with >100 nodes

## 🚀 Future Enhancements

- [ ] Real-time crowd data integration (IoT sensors)
- [ ] Multi-user schedule coordination
- [ ] Historical pattern analysis (ML integration)
- [ ] Mobile app (React Native)
- [ ] Export to Google Calendar/Outlook
- [ ] A* algorithm with heuristics
- [ ] Persistent database (PostgreSQL)
- [ ] User authentication and profiles

## 📝 Viva Defense Tips

### Key Questions to Prepare

1. **Why Dijkstra over Floyd-Warshall for routing?**
   - Answer: Dijkstra is O((V+E) log V) for single-source, much faster than O(V³) for small queries. Use Floyd-Warshall only when needing all-pairs precomputation.

2. **Explain your DP state design for scheduling.**
   - Answer: State dp[i][prev_building] = best preference score for courses 0..i ending at prev_building, incorporating walking cost.

3. **How does Branch & Bound prune the search space?**
   - Answer: Maintains upper bound (best solution so far) and lower bound (optimistic estimate). Prunes branches where lower bound exceeds upper bound.

4. **Parallel speedup is not linear. Why?**
   - Answer: Overhead from thread creation, synchronization, and Amdahl's Law (sequential portions limit speedup).

5. **Time complexity of your complete scheduling pipeline?**
   - Answer: O(n² × V²) worst case (DP with all-pairs distance precomputation), but optimized with Dijkstra caching.

### Demonstration Flow

1. Show live timetable generation
2. Explain algorithm choice (trace through greedy/DP steps)
3. Modify constraints and show adaptation
4. Run benchmarks and interpret plots
5. Walk through code: highlight core algorithm implementations

## 📄 License

MIT License - See LICENSE file

## 🤝 Contributing

This is an academic project. Improvements welcome via pull requests.

## 👨‍💻 Author

Design & Analysis of Algorithms Course Project
Semester 4, 2026

## 📚 References

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
2. Kleinberg, J., & Tardos, É. (2005). *Algorithm Design*. Pearson.
3. FastAPI Documentation: https://fastapi.tiangolo.com/
4. Next.js Documentation: https://nextjs.org/docs

---

**For detailed project report, see [`report/report_template.md`](report/report_template.md)**
