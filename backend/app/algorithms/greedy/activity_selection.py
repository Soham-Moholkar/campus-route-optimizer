"""
Greedy Activity Selection for Course Scheduling.
Unit 3: Greedy Algorithms

Time Complexity: O(n log n) for sorting + O(n) for selection = O(n log n)
Space Complexity: O(n)

Adapts classical activity selection to course slot scheduling with constraints.
"""
from typing import List, Tuple, Dict, Optional


class Activity:
    """Represents a schedulable activity (course slot)."""
    
    def __init__(self, id: int, start: int, end: int, score: float = 1.0, 
                 resource: int = 0, metadata: Dict = None):
        self.id = id
        self.start = start  # Start time in minutes
        self.end = end      # End time in minutes
        self.score = score  # Preference/priority score
        self.resource = resource  # Resource ID (e.g., building_id)
        self.metadata = metadata or {}
    
    def overlaps(self, other: "Activity") -> bool:
        """Check if this activity overlaps with another."""
        return not (self.end <= other.start or self.start >= other.end)
    
    def __repr__(self):
        return f"Activity(id={self.id}, [{self.start}, {self.end}), score={self.score})"


def greedy_activity_selection_by_finish(activities: List[Activity]) -> List[Activity]:
    """
    Classic greedy activity selection by earliest finish time.
    Maximizes number of non-overlapping activities.
    
    Time Complexity: O(n log n)
    
    Args:
        activities: List of activities to schedule
    
    Returns:
        List of selected non-overlapping activities
    """
    if not activities:
        return []
    
    # Sort by end time (greedy choice)
    sorted_activities = sorted(activities, key=lambda a: (a.end, a.start))
    
    selected = [sorted_activities[0]]
    last_end = sorted_activities[0].end
    
    for activity in sorted_activities[1:]:
        if activity.start >= last_end:
            selected.append(activity)
            last_end = activity.end
    
    return selected


def greedy_activity_selection_by_score(activities: List[Activity], 
                                       allow_gaps: int = 0) -> List[Activity]:
    """
    Greedy selection prioritizing high-score activities.
    Useful when preference matters more than count.
    
    Time Complexity: O(n² log n) worst case
    
    Args:
        activities: List of activities
        allow_gaps: Minimum gap (minutes) between activities
    
    Returns:
        List of selected activities with high scores
    """
    if not activities:
        return []
    
    # Sort by score (descending), then by end time
    sorted_activities = sorted(activities, key=lambda a: (-a.score, a.end))
    
    selected = []
    
    for activity in sorted_activities:
        # Check if compatible with all selected activities
        is_compatible = True
        for selected_activity in selected:
            if activity.overlaps(selected_activity):
                is_compatible = False
                break
            # Check gap constraint
            if allow_gaps > 0:
                if selected_activity.end > activity.start:
                    if activity.start - selected_activity.end < allow_gaps:
                        is_compatible = False
                        break
                elif activity.end > selected_activity.start:
                    if selected_activity.start - activity.end < allow_gaps:
                        is_compatible = False
                        break
        
        if is_compatible:
            selected.append(activity)
    
    return selected


def greedy_weighted_interval_scheduling(activities: List[Activity], 
                                       score_ratio: bool = True) -> List[Activity]:
    """
    Greedy approximation for weighted interval scheduling.
    
    Strategy: Sort by score/duration ratio (or just score) and greedily select.
    Not optimal, but fast O(n log n).
    
    Args:
        activities: List of activities with scores
        score_ratio: If True, sort by score/duration ratio
    
    Returns:
        List of selected activities
    """
    if not activities:
        return []
    
    if score_ratio:
        # Sort by score per unit time (density)
        sorted_activities = sorted(
            activities,
            key=lambda a: -a.score / max((a.end - a.start), 1)
        )
    else:
        # Sort by raw score
        sorted_activities = sorted(activities, key=lambda a: (-a.score, a.end))
    
    selected = []
    
    for activity in sorted_activities:
        is_compatible = True
        for selected_activity in selected:
            if activity.overlaps(selected_activity):
                is_compatible = False
                break
        
        if is_compatible:
            selected.append(activity)
    
    return selected


def greedy_course_scheduling(course_activities: Dict[int, List[Activity]], 
                            min_gap: int = 10) -> Tuple[List[Activity], Dict]:
    """
    Greedy course scheduling: select one slot per course.
    
    Strategy: For each course, sort candidate slots by score, pick the first
    that doesn't conflict with already selected slots.
    
    Time Complexity: O(k × n × m) where k=courses, n=avg candidates, m=selected slots
    
    Args:
        course_activities: Dict {course_id: [candidate_activities]}
        min_gap: Minimum gap between classes in minutes
    
    Returns:
        Tuple of (selected activities, stats dict)
    """
    selected = []
    conflicts_resolved = 0
    courses_scheduled = 0
    
    for course_id, candidates in course_activities.items():
        if not candidates:
            continue
        
        # Sort candidates by score (prefer high-score slots)
        sorted_candidates = sorted(candidates, key=lambda a: -a.score)
        
        scheduled = False
        for candidate in sorted_candidates:
            is_compatible = True
            
            for selected_activity in selected:
                # Check overlap
                if candidate.overlaps(selected_activity):
                    is_compatible = False
                    conflicts_resolved += 1
                    break
                
                # Check minimum gap
                if min_gap > 0:
                    gap = min(
                        abs(candidate.start - selected_activity.end),
                        abs(selected_activity.start - candidate.end)
                    )
                    if gap < min_gap and gap > 0:
                        is_compatible = False
                        break
            
            if is_compatible:
                selected.append(candidate)
                courses_scheduled += 1
                scheduled = True
                break
        
        if not scheduled:
            # Could not schedule this course
            pass
    
    total_score = sum(a.score for a in selected)
    
    stats = {
        "total_score": total_score,
        "courses_scheduled": courses_scheduled,
        "conflicts_resolved": conflicts_resolved,
        "total_courses": len(course_activities)
    }
    
    return selected, stats


def job_scheduling_with_deadline(jobs: List[Tuple[int, int, float]]) -> List[int]:
    """
    Job scheduling with deadlines (greedy by profit).
    
    Args:
        jobs: List of (job_id, deadline, profit)
    
    Returns:
        List of scheduled job IDs
    """
    # Sort by profit (descending)
    sorted_jobs = sorted(jobs, key=lambda x: -x[2])
    
    max_deadline = max(job[1] for job in jobs) if jobs else 0
    slots = [-1] * (max_deadline + 1)  # -1 means empty slot
    
    scheduled = []
    total_profit = 0.0
    
    for job_id, deadline, profit in sorted_jobs:
        # Find the latest available slot before deadline
        for slot in range(min(deadline, max_deadline), 0, -1):
            if slots[slot] == -1:
                slots[slot] = job_id
                scheduled.append(job_id)
                total_profit += profit
                break
    
    return scheduled
