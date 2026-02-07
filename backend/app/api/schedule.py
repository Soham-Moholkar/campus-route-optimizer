"""
Scheduling API endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.schedule import ScheduleRequest, ScheduleResult, Course, StudentProfile, ScheduleConstraints
from app.services.schedule_service import schedule_service
from app.services.graph_service import graph_service

router = APIRouter()


class QuickScheduleRequest(BaseModel):
    """Simplified schedule request for quick testing."""
    num_courses: int = Field(default=6, ge=1, le=20, description="Number of courses")
    algorithm: str = Field(default="greedy", description="Algorithm: greedy, dp, exact")
    seed: int = Field(default=42, description="Random seed")


@router.post("/fast", response_model=ScheduleResult)
async def schedule_fast(request: QuickScheduleRequest):
    """
    Generate schedule using greedy algorithm (fast mode).
    
    Time Complexity: O(n log n)
    """
    try:
        # Generate sample courses
        if graph_service.current_graph is None:
            raise HTTPException(status_code=400, detail="No graph loaded. Generate a graph first.")
        
        rooms = graph_service.current_graph.rooms
        courses = schedule_service.generate_sample_courses(
            num_courses=request.num_courses,
            rooms=rooms,
            seed=request.seed
        )
        
        # Create schedule request
        sched_request = ScheduleRequest(
            student_profile=StudentProfile(course_ids=[c.id for c in courses]),
            constraints=ScheduleConstraints(),
            courses=courses,
            algorithm="greedy"
        )
        
        result = schedule_service.schedule_greedy(sched_request)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dp", response_model=ScheduleResult)
async def schedule_dp(request: QuickScheduleRequest):
    """
    Generate schedule using dynamic programming.
    
    Time Complexity: O(n²)
    Better quality than greedy.
    """
    try:
        # Generate sample courses
        if graph_service.current_graph is None:
            raise HTTPException(status_code=400, detail="No graph loaded. Generate a graph first.")
        
        rooms = graph_service.current_graph.rooms
        courses = schedule_service.generate_sample_courses(
            num_courses=request.num_courses,
            rooms=rooms,
            seed=request.seed
        )
        
        sched_request = ScheduleRequest(
            student_profile=StudentProfile(course_ids=[c.id for c in courses]),
            constraints=ScheduleConstraints(),
            courses=courses,
            algorithm="dp"
        )
        
        result = schedule_service.schedule_dp(sched_request)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/exact", response_model=ScheduleResult)
async def schedule_exact(request: QuickScheduleRequest):
    """
    Generate optimal schedule using branch & bound.
    
    Time Complexity: O(k^n) with pruning
    Recommended for <=10 courses.
    """
    try:
        if request.num_courses > 12:
            raise HTTPException(
                status_code=400,
                detail="Exact mode supports maximum 12 courses. Use DP mode for larger instances."
            )
        
        # Generate sample courses
        if graph_service.current_graph is None:
            raise HTTPException(status_code=400, detail="No graph loaded. Generate a graph first.")
        
        rooms = graph_service.current_graph.rooms
        courses = schedule_service.generate_sample_courses(
            num_courses=request.num_courses,
            rooms=rooms,
            seed=request.seed
        )
        
        # Get walking distances
        walking_distances = graph_service.get_distance_matrix()
        
        sched_request = ScheduleRequest(
            student_profile=StudentProfile(course_ids=[c.id for c in courses]),
            constraints=ScheduleConstraints(),
            courses=courses,
            algorithm="exact"
        )
        
        result = schedule_service.schedule_exact(sched_request, walking_distances)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/custom", response_model=ScheduleResult)
async def schedule_custom(request: ScheduleRequest):
    """
    Generate schedule with custom courses and constraints.
    
    Allows full control over courses, constraints, and algorithm choice.
    """
    try:
        if request.algorithm == "greedy":
            result = schedule_service.schedule_greedy(request)
        elif request.algorithm == "dp":
            result = schedule_service.schedule_dp(request)
        elif request.algorithm == "exact":
            if len(request.courses) > 12:
                raise HTTPException(
                    status_code=400,
                    detail="Exact mode supports maximum 12 courses."
                )
            walking_distances = graph_service.get_distance_matrix()
            result = schedule_service.schedule_exact(request, walking_distances)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown algorithm: {request.algorithm}")
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/timeslots")
async def get_timeslots():
    """Get available time slots."""
    return {"timeslots": schedule_service.timeslots}
