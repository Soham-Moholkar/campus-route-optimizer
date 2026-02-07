"""
Schedule service for timetable optimization.
"""
from typing import Dict, List, Tuple
import random
import time
from app.models.schedule import (
    Course, CandidateSlot, TimeSlot, ScheduleRequest, ScheduleResult, SelectedSlot
)
from app.algorithms.greedy.activity_selection import Activity, greedy_course_scheduling
from app.algorithms.dp.weighted_interval import WeightedInterval, course_scheduling_dp
from app.algorithms.exact.backtracking import branch_and_bound_schedule


class ScheduleService:
    """Service for course scheduling operations."""
    
    def __init__(self):
        self.timeslots = self._generate_timeslots()
        self.timeslot_map = {ts.id: ts for ts in self.timeslots}
    
    def _generate_timeslots(self) -> List[TimeSlot]:
        """Generate standard weekly timeslots."""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        slots = []
        slot_id = 0
        
        # 9:00 AM to 5:00 PM, 1-hour slots
        for day in days:
            for hour in range(9, 17):
                start_min = hour * 60
                end_min = (hour + 1) * 60
                slots.append(TimeSlot(
                    id=slot_id,
                    day=day,
                    start_min=start_min,
                    end_min=end_min
                ))
                slot_id += 1
        
        return slots
    
    def generate_sample_courses(self, num_courses: int, rooms: List, 
                               seed: int = 42) -> List[Course]:
        """
        Generate sample courses with candidate slots.
        
        Args:
            num_courses: Number of courses to generate
            rooms: List of available rooms
            seed: Random seed
        
        Returns:
            List of courses
        """
        random.seed(seed)
        
        course_names = [
            "Data Structures", "Algorithms", "Database Systems", "Operating Systems",
            "Computer Networks", "Software Engineering", "Web Development", "Machine Learning",
            "Artificial Intelligence", "Computer Architecture", "Compiler Design", "Theory of Computation",
            "Computer Graphics", "Distributed Systems", "Cloud Computing", "Cybersecurity",
            "Mobile App Development", "Data Science", "Digital Logic", "Discrete Mathematics"
        ]
        
        courses = []
        
        for i in range(num_courses):
            course_name = course_names[i % len(course_names)]
            if i >= len(course_names):
                course_name = f"{course_name} {i // len(course_names) + 1}"
            
            expected_strength = random.randint(30, 150)
            
            # Generate 5-10 candidate slots
            num_candidates = random.randint(5, 10)
            candidates = []
            
            for _ in range(num_candidates):
                timeslot = random.choice(self.timeslots)
                room = random.choice([r for r in rooms if r.capacity >= expected_strength])
                preference_score = random.uniform(50, 100)
                
                candidates.append(CandidateSlot(
                    timeslot_id=timeslot.id,
                    room_id=room.id,
                    building_id=room.building_id,
                    preference_score=preference_score
                ))
            
            courses.append(Course(
                id=i,
                name=course_name,
                expected_strength=expected_strength,
                candidate_slots=candidates
            ))
        
        return courses
    
    def schedule_greedy(self, request: ScheduleRequest) -> ScheduleResult:
        """
        Generate schedule using greedy algorithm.
        
        Time Complexity: O(n × m × k) where n=courses, m=candidates, k=selected
        
        Args:
            request: Schedule request
        
        Returns:
            Schedule result
        """
        start_time = time.perf_counter()
        
        # Convert to Activity objects
        course_activities = {}
        
        for course in request.courses:
            activities = []
            for i, candidate in enumerate(course.candidate_slots):
                timeslot = self.timeslot_map[candidate.timeslot_id]
                
                activity = Activity(
                    id=i,
                    start=timeslot.start_min + (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(timeslot.day) * 24 * 60),
                    end=timeslot.end_min + (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(timeslot.day) * 24 * 60),
                    score=candidate.preference_score,
                    resource=candidate.building_id,
                    metadata={
                        "course_id": course.id,
                        "course_name": course.name,
                        "candidate_idx": i,
                        "timeslot": timeslot,
                        "room_id": candidate.room_id,
                        "building_id": candidate.building_id
                    }
                )
                activities.append(activity)
            
            course_activities[course.id] = activities
        
        # Apply greedy scheduling
        selected_activities, stats = greedy_course_scheduling(
            course_activities,
            min_gap=request.constraints.min_gap_minutes or 10
        )
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        # Convert to SelectedSlot objects
        selected_slots = []
        
        for activity in selected_activities:
            timeslot = activity.metadata["timeslot"]
            selected_slots.append(SelectedSlot(
                course_id=activity.metadata["course_id"],
                course_name=activity.metadata["course_name"],
                timeslot_id=timeslot.id,
                room_id=activity.metadata["room_id"],
                building_id=activity.metadata["building_id"],
                day=timeslot.day,
                start_min=timeslot.start_min,
                end_min=timeslot.end_min,
                preference_score=activity.score
            ))
        
        return ScheduleResult(
            selected_slots=selected_slots,
            total_preference=stats["total_score"],
            walking_cost=0.0,  # Computed separately
            idle_time=0,  # Computed separately
            conflicts_resolved=stats["conflicts_resolved"],
            algorithm_used="greedy",
            computation_time_ms=elapsed_ms,
            feasible=True
        )
    
    def schedule_dp(self, request: ScheduleRequest) -> ScheduleResult:
        """
        Generate schedule using dynamic programming.
        
        Time Complexity: O(n × m²)
        
        Args:
            request: Schedule request
        
        Returns:
            Schedule result
        """
        start_time = time.perf_counter()
        
        # Convert to WeightedInterval objects
        course_intervals = {}
        
        for course in request.courses:
            intervals = []
            for i, candidate in enumerate(course.candidate_slots):
                timeslot = self.timeslot_map[candidate.timeslot_id]
                
                # Convert to minutes from start of week
                start_abs = (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(timeslot.day) * 24 * 60) + timeslot.start_min
                end_abs = (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(timeslot.day) * 24 * 60) + timeslot.end_min
                
                interval = WeightedInterval(
                    id=i,
                    start=start_abs,
                    end=end_abs,
                    weight=candidate.preference_score,
                    metadata={
                        "course_id": course.id,
                        "course_name": course.name,
                        "timeslot": timeslot,
                        "room_id": candidate.room_id,
                        "building_id": candidate.building_id
                    }
                )
                intervals.append(interval)
            
            course_intervals[course.id] = intervals
        
        # Apply DP scheduling
        total_score, selected_by_course, stats = course_scheduling_dp(course_intervals)
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        # Convert to SelectedSlot objects
        selected_slots = []
        
        for course_id, interval in selected_by_course.items():
            timeslot = interval.metadata["timeslot"]
            selected_slots.append(SelectedSlot(
                course_id=course_id,
                course_name=interval.metadata["course_name"],
                timeslot_id=timeslot.id,
                room_id=interval.metadata["room_id"],
                building_id=interval.metadata["building_id"],
                day=timeslot.day,
                start_min=timeslot.start_min,
                end_min=timeslot.end_min,
                preference_score=interval.weight
            ))
        
        return ScheduleResult(
            selected_slots=selected_slots,
            total_preference=total_score,
            walking_cost=0.0,
            idle_time=0,
            conflicts_resolved=0,
            algorithm_used="dp",
            computation_time_ms=elapsed_ms,
            feasible=True
        )
    
    def schedule_exact(self, request: ScheduleRequest, 
                      walking_distances: Dict[Tuple[int, int], float] = None) -> ScheduleResult:
        """
        Generate optimal schedule using branch & bound.
        
        Time Complexity: O(k^n) with pruning
        Recommended for <=10 courses.
        
        Args:
            request: Schedule request
            walking_distances: Distance matrix
        
        Returns:
            Schedule result
        """
        start_time = time.perf_counter()
        
        if len(request.courses) > 12:
            # Fallback to DP for large instances
            return self.schedule_dp(request)
        
        # Prepare data for backtracking
        course_ids = [c.id for c in request.courses]
        course_map = {c.id: c for c in request.courses}
        
        candidates_map = {}
        for course in request.courses:
            candidates_map[course.id] = [
                {
                    "timeslot_id": cs.timeslot_id,
                    "room_id": cs.room_id,
                    "building_id": cs.building_id,
                    "preference_score": cs.preference_score
                }
                for cs in course.candidate_slots
            ]
        
        timeslot_dict_map = {
            ts.id: {
                "day": ts.day,
                "start_min": ts.start_min,
                "end_min": ts.end_min
            }
            for ts in self.timeslots
        }
        
        if walking_distances is None:
            walking_distances = {}
        
        # Run branch & bound
        best_state, stats = branch_and_bound_schedule(
            course_ids,
            candidates_map,
            timeslot_dict_map,
            walking_distances,
            timeout_seconds=15.0
        )
        
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        if best_state is None:
            # No solution found
            return ScheduleResult(
                selected_slots=[],
                total_preference=0.0,
                walking_cost=0.0,
                idle_time=0,
                conflicts_resolved=0,
                algorithm_used="exact",
                computation_time_ms=elapsed_ms,
                feasible=False
            )
        
        # Convert to SelectedSlot objects
        selected_slots = []
        total_preference = 0.0
        
        for course_id, candidate_idx in best_state.assignments.items():
            candidate = candidates_map[course_id][candidate_idx]
            timeslot = self.timeslot_map[candidate["timeslot_id"]]
            
            selected_slots.append(SelectedSlot(
                course_id=course_id,
                course_name=course_map[course_id].name,
                timeslot_id=candidate["timeslot_id"],
                room_id=candidate["room_id"],
                building_id=candidate["building_id"],
                day=timeslot.day,
                start_min=timeslot.start_min,
                end_min=timeslot.end_min,
                preference_score=candidate["preference_score"]
            ))
            total_preference += candidate["preference_score"]
        
        return ScheduleResult(
            selected_slots=selected_slots,
            total_preference=total_preference,
            walking_cost=best_state.walking_cost,
            idle_time=0,
            conflicts_resolved=0,
            algorithm_used="exact",
            computation_time_ms=elapsed_ms,
            feasible=True
        )


# Global instance
schedule_service = ScheduleService()
