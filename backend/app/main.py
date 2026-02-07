"""
FastAPI main application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes, schedule, benchmarks

app = FastAPI(
    title="SmartCampus Path + Slot Optimizer",
    description="Campus-scale optimization engine for timetables and routing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, tags=["Graph & Routing"])
app.include_router(schedule.router, prefix="/schedule", tags=["Scheduling"])
app.include_router(benchmarks.router, prefix="/bench", tags=["Benchmarks"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "SmartCampus Path + Slot Optimizer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
