# SmartCampus Optimizer - Quick Setup Guide

## Prerequisites

Ensure you have:
- Python 3.11+ (`python --version`)
- Node.js 18+ (`node --version`)
- pip (`pip --version`)
- npm (`npm --version`)

## Step-by-Step Setup

### 1. Backend Setup (5 minutes)

```powershell
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; print('FastAPI installed successfully')"
```

### 2. Start Backend Server

```powershell
# From backend directory
uvicorn app.main:app --reload

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete.
```

**Test backend:** Open http://localhost:8000/docs in your browser

### 3. Frontend Setup (New Terminal - 5 minutes)

```powershell
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Expected: Installing packages... (takes 2-3 minutes)
```

### 4. Start Frontend Server

```powershell
# From frontend directory
npm run dev

# Expected output:
# ▲ Next.js 14.1.0
# - Local:        http://localhost:3000
```

**Test frontend:** Open http://localhost:3000 in your browser

---

## First Run Demo (5 minutes)

### Demo Workflow

1. **Generate Campus Graph**
   - Go to http://localhost:3000/campus-map
   - Click "Generate Campus Graph"
   - Wait 1-2 seconds
   - You should see 20 buildings

2. **Compute Shortest Path**
   - Select start building (e.g., "Main Building")
   - Select end building (e.g., "Library")
   - Choose algorithm "Dijkstra"
   - Click "Compute Shortest Path"
   - Path will be highlighted on map

3. **Generate Timetable**
   - Go to http://localhost:3000/timetable
   - Set courses to 6
   - Choose "Greedy (Fast)"
   - Click "Generate Schedule"
   - View timetable in grid format

4. **Run Benchmarks**
   - Go to http://localhost:3000/benchmarks
   - Select "Sorting (Merge vs Quick)"
   - Click "Run Benchmark"
   - View results table and note saved files

---

## Troubleshooting

### Backend Issues

**Error: "ModuleNotFoundError: No module named 'fastapi'"**
```powershell
pip install -r requirements.txt
```

**Error: "Address already in use"**
```powershell
# Change port
uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

**Error: "Cannot find module"**
```powershell
rm -rf node_modules
rm package-lock.json
npm install
```

**Error: "Port 3000 is in use"**
```powershell
# Frontend will auto-prompt for port 3001
# Or manually specify:
npm run dev -- -p 3001
```

**Error: "Failed to fetch"**
- Ensure backend is running on http://localhost:8000
- Check CORS settings in `backend/app/main.py`

---

## Running Tests

### Backend Tests

```powershell
cd backend
pytest tests/ -v

# Expected: 16 tests passed
```

### Test Individual Modules

```powershell
pytest tests/test_dijkstra.py -v
pytest tests/test_floyd_warshall.py -v
pytest tests/test_scheduling.py -v
```

---

## Running Benchmarks

### Option 1: Via Frontend UI
- Navigate to http://localhost:3000/benchmarks
- Select suite and click "Run Benchmark"

### Option 2: Via Command Line

```powershell
cd scripts
python run_all_benchmarks.py

# Results saved to: backend/app/benchmarks/results/
```

### Option 3: Via API

```powershell
# Using curl or Invoke-WebRequest
curl -X POST "http://localhost:8000/bench/run" `
  -H "Content-Type: application/json" `
  -d '{"suite": "dijkstra", "trials": 5, "seed": 42}'
```

---

## Generating Sample Data

```powershell
cd scripts
python generate_sample_data.py

# Output: generated_campus.json in backend/app/data/
```

---

## API Documentation

Once backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

**Graph & Routing:**
- `POST /generate/campus_graph` - Generate campus
- `POST /route/shortest` - Compute path
- `POST /crowd/simulate` - Simulate congestion

**Scheduling:**
- `POST /schedule/fast` - Greedy scheduling
- `POST /schedule/dp` - DP scheduling
- `POST /schedule/exact` - Exact scheduling

**Benchmarks:**
- `POST /bench/run` - Run benchmarks
- `GET /bench/results` - List results

---

## Project Structure Quick Reference

```
smartcampus-optimizer/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI app entry point
│   │   ├── algorithms/  # Core algorithm implementations
│   │   ├── api/         # API route handlers
│   │   ├── models/      # Pydantic data models
│   │   └── services/    # Business logic layer
│   └── tests/           # Unit tests (pytest)
├── frontend/            # Next.js frontend
│   ├── app/             # Pages (App Router)
│   ├── components/      # React components
│   └── lib/             # API client & types
├── scripts/             # Utility scripts
└── report/              # Project documentation
```

---

## Performance Expectations

**Backend:**
- Graph generation (20 nodes): <100ms
- Dijkstra shortest path: <2ms
- Greedy scheduling (10 courses): <10ms
- DP scheduling (10 courses): <50ms

**Frontend:**
- Page load: <500ms
- API request: <100ms (+ backend time)
- Graph rendering: <200ms

---

## Common Development Tasks

### Add New Algorithm

1. Implement in `backend/app/algorithms/<category>/`
2. Add service method in `backend/app/services/`
3. Create API endpoint in `backend/app/api/`
4. Add frontend UI in `frontend/app/<page>/`

### Add New Benchmark

1. Add suite in `backend/app/benchmarks/benchmark_runner.py`
2. Update benchmark config model if needed
3. Frontend will automatically support it

### Modify Graph Visualization

Edit `frontend/components/CampusGraph.tsx`:
- SVG rendering in the component
- Change colors, sizes, labels

---

## Deployment Notes

### Backend (Production)

```powershell
# Install production server
pip install gunicorn

# Run with multiple workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend (Production)

```powershell
# Build for production
npm run build

# Start production server
npm start
```

---

## Additional Resources

- **README.md** - Comprehensive project documentation
- **report/report_template.md** - Full project report
- **Backend API Docs** - http://localhost:8000/docs
- **Algorithm Explorer** - http://localhost:3000/algorithms

---

## Support

For issues:
1. Check this setup guide
2. Review error messages carefully
3. Verify Python and Node versions
4. Ensure all dependencies installed

---

**Happy Coding! 🚀**
