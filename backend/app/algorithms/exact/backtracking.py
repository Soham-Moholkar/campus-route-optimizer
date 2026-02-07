"""
Backtracking and Branch & Bound for Exact Course Scheduling.
Unit 6: Backtracking and Branch & Bound

Time Complexity: O(k^n) worst case where k = avg candidates per course
Space Complexity: O(n) for recursion stack

Provides optimal solutions for small instances (<=12 courses recommended).
"""
from typing import List, Dict, Tuple, Optional
import time


class SchedulingState:
    """State representation for backtracking search."""
    
    def __init__(self, course_ids: List[int]):
        self.course_ids = course_ids
        self.assignments = {}  # {course_id: candidate_index}
        self.score = 0.0
        self.walking_cost = 0.0
        self.level = 0  # Current course being assigned
    
    def copy(self):
        """Deep copy of state."""
        new_state = SchedulingState(self.course_ids)
        new_state.assignments = self.assignments.copy()
        new_state.score = self.score
        new_state.walking_cost = self.walking_cost
        new_state.level = self.level
        return new_state


def is_feasible_assignment(state: SchedulingState, course_id: int, candidate_idx: int,
                          candidates_map: Dict[int, List[Dict]], 
                          timeslot_map: Dict[int, Dict]) -> bool:
    """
    Check if assigning candidate_idx to course_id is feasible.
    
    Checks for time slot conflicts with already assigned courses.
    
    Args:
        state: Current scheduling state
        course_id: Course to assign
        candidate_idx: Candidate slot index
        candidates_map: {course_id: [candidate_slots]}
        timeslot_map: {timeslot_id: {day, start_min, end_min}}
    
    Returns:
        True if assignment is feasible
    """
    candidate = candidates_map[course_id][candidate_idx]
    candidate_timeslot = timeslot_map[candidate["timeslot_id"]]
    
    # Check against all assigned courses
    for assigned_course_id, assigned_idx in state.assignments.items():
        if assigned_course_id == course_id:
            continue
        
        assigned_candidate = candidates_map[assigned_course_id][assigned_idx]
        assigned_timeslot = timeslot_map[assigned_candidate["timeslot_id"]]
        
        # Check overlap
        if candidate_timeslot["day"] == assigned_timeslot["day"]:
            # Same day, check time overlap
            if not (candidate_timeslot["end_min"] <= assigned_timeslot["start_min"] or
                    candidate_timeslot["start_min"] >= assigned_timeslot["end_min"]):
                return False  # Conflict
    
    return True


def compute_objective(state: SchedulingState, candidates_map: Dict[int, List[Dict]], 
                     walking_distances: Dict[Tuple[int, int], float],
                     timeslot_map: Dict[int, Dict],
                     weight_preference: float = 0.5,
                     weight_walking: float = 0.5) -> float:
    """
    Compute objective function value for current state.
    
    Objective: maximize preference - (normalized_walking_cost)
    
    Args:
        state: Current state
        candidates_map: Candidate mappings
        walking_distances: {(building1, building2): distance}
        timeslot_map: Timeslot information
        weight_preference: Weight for preference component
        weight_walking: Weight for walking cost component
    
    Returns:
        Objective value (higher is better)
    """
    total_preference = 0.0
    total_walking = 0.0
    
    # Sort assignments by time for sequential walking cost
    sorted_courses = sorted(state.assignments.items(), 
                          key=lambda x: timeslot_map[candidates_map[x[0]][x[1]]["timeslot_id"]]["start_min"])
    
    for course_id, candidate_idx in sorted_courses:
        candidate = candidates_map[course_id][candidate_idx]
        total_preference += candidate["preference_score"]
    
    # Compute walking cost between consecutive classes
    for i in range(len(sorted_courses) - 1):
        course1_id, idx1 = sorted_courses[i]
        course2_id, idx2 = sorted_courses[i + 1]
        
        building1 = candidates_map[course1_id][idx1]["building_id"]
        building2 = candidates_map[course2_id][idx2]["building_id"]
        
        # Check if on the same day
        ts1 = timeslot_map[candidates_map[course1_id][idx1]["timeslot_id"]]
        ts2 = timeslot_map[candidates_map[course2_id][idx2]["timeslot_id"]]
        
        if ts1["day"] == ts2["day"]:
            distance = walking_distances.get((building1, building2), 0.0)
            total_walking += distance
    
    # Normalize (assume max preference = 100 per course, max walking = 2000m)
    norm_preference = total_preference / (len(sorted_courses) * 100.0) if sorted_courses else 0.0
    norm_walking = total_walking / 2000.0
    
    objective = weight_preference * norm_preference - weight_walking * norm_walking
    
    return objective


def backtracking_schedule(course_ids: List[int], 
                         candidates_map: Dict[int, List[Dict]],
                         timeslot_map: Dict[int, Dict],
                         walking_distances: Dict[Tuple[int, int], float],
                         timeout_seconds: float = 10.0) -> Tuple[Optional[SchedulingState], Dict]:
    """
    Backtracking algorithm for exact course scheduling.
    
    Time Complexity: O(k^n) where k = avg candidates, n = courses
    
    Args:
        course_ids: List of courses to schedule
        candidates_map: {course_id: [candidate_slots]}
        timeslot_map: {timeslot_id: timeslot_info}
        walking_distances: Distance matrix
        timeout_seconds: Maximum runtime
    
    Returns:
        Tuple of (best_state, stats)
    """
    start_time = time.time()
    best_state = None
    best_objective = float('-inf')
    nodes_explored = 0
    
    def backtrack(state: SchedulingState) -> None:
        nonlocal best_state, best_objective, nodes_explored
        
        nodes_explored += 1
        
        # Check timeout
        if time.time() - start_time > timeout_seconds:
            return
        
        # Base case: all courses assigned
        if state.level == len(course_ids):
            objective = compute_objective(state, candidates_map, walking_distances, timeslot_map)
            if objective > best_objective:
                best_objective = objective
                best_state = state.copy()
            return
        
        # Recursive case: try assigning next course
        course_id = course_ids[state.level]
        candidates = candidates_map.get(course_id, [])
        
        for candidate_idx in range(len(candidates)):
            # Check feasibility
            if is_feasible_assignment(state, course_id, candidate_idx, candidates_map, timeslot_map):
                # Make assignment
                state.assignments[course_id] = candidate_idx
                state.level += 1
                
                # Recurse
                backtrack(state)
                
                # Backtrack
                state.level -= 1
                del state.assignments[course_id]
    
    initial_state = SchedulingState(course_ids)
    backtrack(initial_state)
    
    stats = {
        "nodes_explored": nodes_explored,
        "time_seconds": time.time() - start_time,
        "best_objective": best_objective,
        "timed_out": time.time() - start_time >= timeout_seconds
    }
    
    return best_state, stats


def branch_and_bound_schedule(course_ids: List[int], 
                              candidates_map: Dict[int, List[Dict]],
                              timeslot_map: Dict[int, Dict],
                              walking_distances: Dict[Tuple[int, int], float],
                              timeout_seconds: float = 30.0) -> Tuple[Optional[SchedulingState], Dict]:
    """
    Branch and Bound algorithm for exact course scheduling.
    
    Uses upper bound (best so far) and lower bound (optimistic estimate) for pruning.
    
    Time Complexity: O(k^n) worst case, but significantly pruned
    
    Args:
        course_ids: List of courses to schedule
        candidates_map: {course_id: [candidate_slots]}
        timeslot_map: {timeslot_id: timeslot_info}
        walking_distances: Distance matrix
        timeout_seconds: Maximum runtime
    
    Returns:
        Tuple of (best_state, stats)
    """
    start_time = time.time()
    best_state = None
    best_objective = float('-inf')  # Upper bound
    nodes_explored = 0
    nodes_pruned = 0
    
    def compute_upper_bound(state: SchedulingState) -> float:
        """
        Compute optimistic upper bound for current state.
        Assumes all remaining courses get max preference with zero walking cost.
        """
        current_obj = compute_objective(state, candidates_map, walking_distances, timeslot_map)
        
        # Add optimistic contribution from unassigned courses
        remaining = len(course_ids) - state.level
        max_possible_preference = remaining * 100.0 / (len(course_ids) * 100.0) * 0.5  # Normalized
        
        return current_obj + max_possible_preference
    
    def branch_bound(state: SchedulingState) -> None:
        nonlocal best_state, best_objective, nodes_explored, nodes_pruned
        
        nodes_explored += 1
        
        # Check timeout
        if time.time() - start_time > timeout_seconds:
            return
        
        # Compute upper bound for this node
        upper = compute_upper_bound(state)
        
        # Prune if upper bound <= current best (maximization)
        if upper <= best_objective:
            nodes_pruned += 1
            return
        
        # Base case: all courses assigned
        if state.level == len(course_ids):
            objective = compute_objective(state, candidates_map, walking_distances, timeslot_map)
            if objective > best_objective:
                best_objective = objective
                best_state = state.copy()
            return
        
        # Recursive case: branch on next course
        course_id = course_ids[state.level]
        candidates = candidates_map.get(course_id, [])
        
        # Sort candidates by preference (best first) for better pruning
        sorted_candidates = sorted(enumerate(candidates), 
                                  key=lambda x: -x[1]["preference_score"])
        
        for candidate_idx, _ in sorted_candidates:
            # Check feasibility
            if is_feasible_assignment(state, course_id, candidate_idx, candidates_map, timeslot_map):
                # Make assignment
                state.assignments[course_id] = candidate_idx
                state.level += 1
                
                # Recurse
                branch_bound(state)
                
                # Backtrack
                state.level -= 1
                del state.assignments[course_id]
    
    initial_state = SchedulingState(course_ids)
    branch_bound(initial_state)
    
    stats = {
        "nodes_explored": nodes_explored,
        "nodes_pruned": nodes_pruned,
        "time_seconds": time.time() - start_time,
        "best_objective": best_objective,
        "timed_out": time.time() - start_time >= timeout_seconds,
        "pruning_ratio": nodes_pruned / max(nodes_explored, 1)
    }
    
    return best_state, stats


def n_queens_solver(n: int) -> List[List[int]]:
    """
    N-Queens problem solver using backtracking.
    
    Included as a classic backtracking example for viva defense.
    
    Time Complexity: O(n!)
    
    Args:
        n: Board size
    
    Returns:
        List of solutions (each solution is a list of column positions)
    """
    solutions = []
    
    def is_safe(board: List[int], row: int, col: int) -> bool:
        """Check if placing queen at (row, col) is safe."""
        for i in range(row):
            # Check column and diagonals
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True
    
    def solve(board: List[int], row: int):
        """Backtracking search."""
        if row == n:
            solutions.append(board.copy())
            return
        
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve(board, row + 1)
                board[row] = -1  # Backtrack
    
    initial_board = [-1] * n
    solve(initial_board, 0)
    
    return solutions
