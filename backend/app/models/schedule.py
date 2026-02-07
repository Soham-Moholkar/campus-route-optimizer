"""
Scheduling data models.
Represents courses, time slots, and schedule optimization requests/results.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class TimeSlot(BaseModel):
    """Represents a specific time period in the week."""
    id: int = Field(..., description="Unique timeslot identifier")
    day: str = Field(..., description="Day of week (Monday-Friday)")
    start_min: int = Field(..., description="Start time in minutes from midnight")
    end_min: int = Field(..., description="End time in minutes from midnight")

    def overlaps(self, other: "TimeSlot") -> bool:
        """Check if this timeslot overlaps with another."""
        if self.day != other.day:
            return False
        return not (self.end_min <= other.start_min or self.start_min >= other.end_min)

    @property
    def duration(self) -> int:
        """Duration in minutes."""
        return self.end_min - self.start_min


class CandidateSlot(BaseModel):
    """A possible slot assignment for a course."""
    timeslot_id: int = Field(..., description="Time slot ID")
    room_id: int = Field(..., description="Room ID")
    building_id: int = Field(..., description="Building node ID")
    preference_score: float = Field(..., description="Student preference score (0-100)")


class Course(BaseModel):
    """Represents a course offering."""
    id: int = Field(..., description="Unique course identifier")
    name: str = Field(..., description="Course name/code")
    expected_strength: int = Field(..., description="Expected number of students")
    candidate_slots: List[CandidateSlot] = Field(..., description="Possible slot assignments")


class StudentProfile(BaseModel):
    """Student preferences and constraints."""
    id: int = Field(default=0, description="Student identifier")
    course_ids: List[int] = Field(..., description="List of course IDs to schedule")
    start_location_node: int = Field(default=0, description="Starting location (e.g., hostel)")
    preference_weights: Dict[str, float] = Field(
        default_factory=lambda: {
            "preference_score": 0.4,
            "walking_distance": 0.3,
            "idle_time": 0.3
        },
        description="Weights for optimization objectives"
    )


class ScheduleConstraints(BaseModel):
    """Hard and soft constraints for scheduling."""
    max_walking_distance: Optional[float] = Field(default=2000.0, description="Max walking distance in meters")
    max_idle_minutes: Optional[int] = Field(default=120, description="Max idle time between classes")
    min_gap_minutes: Optional[int] = Field(default=10, description="Minimum gap for walking")


class ScheduleRequest(BaseModel):
    """Request for schedule generation."""
    student_profile: StudentProfile
    constraints: ScheduleConstraints = Field(default_factory=ScheduleConstraints)
    courses: List[Course]
    algorithm: str = Field(default="greedy", description="Algorithm choice: greedy, dp, exact")


class SelectedSlot(BaseModel):
    """A chosen slot for a course in the final schedule."""
    course_id: int
    course_name: str
    timeslot_id: int
    room_id: int
    building_id: int
    day: str
    start_min: int
    end_min: int
    preference_score: float


class ScheduleResult(BaseModel):
    """Result of schedule optimization."""
    selected_slots: List[SelectedSlot] = Field(..., description="Chosen schedule")
    total_preference: float = Field(..., description="Sum of preference scores")
    walking_cost: float = Field(..., description="Total walking distance in meters")
    idle_time: int = Field(..., description="Total idle time in minutes")
    conflicts_resolved: int = Field(default=0, description="Number of conflicts handled")
    algorithm_used: str = Field(..., description="Algorithm that generated this schedule")
    computation_time_ms: float = Field(..., description="Time taken to compute")
    feasible: bool = Field(default=True, description="Whether schedule satisfies all hard constraints")

    class Config:
        json_schema_extra = {
            "example": {
                "selected_slots": [
                    {
                        "course_id": 0,
                        "course_name": "DAA",
                        "timeslot_id": 0,
                        "room_id": 0,
                        "building_id": 1,
                        "day": "Monday",
                        "start_min": 540,
                        "end_min": 600,
                        "preference_score": 85.0
                    }
                ],
                "total_preference": 425.0,
                "walking_cost": 850.0,
                "idle_time": 30,
                "conflicts_resolved": 2,
                "algorithm_used": "greedy",
                "computation_time_ms": 5.2,
                "feasible": True
            }
        }
