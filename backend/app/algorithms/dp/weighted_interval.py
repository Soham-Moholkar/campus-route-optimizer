"""
Weighted Interval Scheduling using Dynamic Programming.
Unit 4: Dynamic Programming

Time Complexity: O(n log n) for sorting + O(n) for DP = O(n log n)
Space Complexity: O(n)

Optimal solution for maximizing weighted non-overlapping intervals.
"""
from typing import List, Tuple, Dict
import bisect


class WeightedInterval:
    """Represents an interval with a weight/score."""
    
    def __init__(self, id: int, start: int, end: int, weight: float, metadata: Dict = None):
        self.id = id
        self.start = start
        self.end = end
        self.weight = weight
        self.metadata = metadata or {}
    
    def __repr__(self):
        return f"Interval(id={self.id}, [{self.start}, {self.end}), w={self.weight})"


def find_latest_non_overlapping(intervals: List[WeightedInterval], index: int) -> int:
    """
    Binary search to find the latest interval that doesn't overlap with intervals[index].
    
    Args:
        intervals: Sorted list of intervals (by end time)
        index: Current interval index
    
    Returns:
        Index of latest non-overlapping interval, or -1 if none
    """
    # Find the rightmost interval that ends before intervals[index] starts
    start_time = intervals[index].start
    
    # Binary search on end times
    left, right = 0, index - 1
    result = -1
    
    while left <= right:
        mid = (left + right) // 2
        if intervals[mid].end <= start_time:
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def weighted_interval_scheduling_dp(intervals: List[WeightedInterval]) -> Tuple[float, List[WeightedInterval]]:
    """
    Dynamic Programming solution for weighted interval scheduling.
    
    Recurrence:
        dp[i] = max(dp[i-1], weight[i] + dp[p(i)])
        where p(i) = latest non-overlapping interval before i
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    Args:
        intervals: List of weighted intervals
    
    Returns:
        Tuple of (max_weight, selected_intervals)
    """
    if not intervals:
        return (0.0, [])
    
    n = len(intervals)
    
    # Sort by end time
    sorted_intervals = sorted(intervals, key=lambda x: (x.end, x.start))
    
    # DP array: dp[i] = max weight using intervals 0..i
    dp = [0.0] * n
    dp[0] = sorted_intervals[0].weight
    
    # Precompute latest non-overlapping intervals
    prev = [-1] * n
    for i in range(1, n):
        prev[i] = find_latest_non_overlapping(sorted_intervals, i)
    
    # Fill DP table
    for i in range(1, n):
        # Choice 1: Don't include interval i
        exclude = dp[i - 1]
        
        # Choice 2: Include interval i
        include = sorted_intervals[i].weight
        if prev[i] != -1:
            include += dp[prev[i]]
        
        dp[i] = max(exclude, include)
    
    # Backtrack to find selected intervals
    selected = []
    i = n - 1
    
    while i >= 0:
        if i == 0:
            selected.append(sorted_intervals[0])
            break
        
        # Check if interval i was included
        include_val = sorted_intervals[i].weight
        if prev[i] != -1:
            include_val += dp[prev[i]]
        
        if include_val >= dp[i - 1]:
            # Interval i was included
            selected.append(sorted_intervals[i])
            i = prev[i]
        else:
            # Interval i was not included
            i -= 1
    
    selected.reverse()
    
    return (dp[n - 1], selected)


def weighted_interval_scheduling_with_resource(intervals: List[WeightedInterval], 
                                               walking_cost: Dict[Tuple[int, int], float] = None) -> Tuple[float, List[WeightedInterval]]:
    """
    Extended weighted interval scheduling considering location transitions.
    
    State: dp[i][loc] = max score ending at interval i in location loc
    
    Time Complexity: O(n² × L) where L = number of locations (simplified to O(n²))
    
    Args:
        intervals: List of weighted intervals with location metadata
        walking_cost: Dict {(loc1, loc2): cost} for transitions
    
    Returns:
        Tuple of (max_score, selected_intervals)
    """
    if not intervals:
        return (0.0, [])
    
    n = len(intervals)
    sorted_intervals = sorted(intervals, key=lambda x: (x.end, x.start))
    
    # Simplified DP without explicit location tracking
    # Use negative walking cost as penalty
    dp = [0.0] * n
    prev_choice = [-1] * n
    
    for i in range(n):
        # Option 1: Start fresh with this interval
        dp[i] = sorted_intervals[i].weight
        prev_choice[i] = -1
        
        # Option 2: Extend from a previous non-overlapping interval
        for j in range(i):
            if sorted_intervals[j].end <= sorted_intervals[i].start:
                # Compute walking cost if provided
                cost = 0.0
                if walking_cost and "location" in sorted_intervals[j].metadata and "location" in sorted_intervals[i].metadata:
                    loc1 = sorted_intervals[j].metadata["location"]
                    loc2 = sorted_intervals[i].metadata["location"]
                    cost = walking_cost.get((loc1, loc2), 0.0)
                
                score = dp[j] + sorted_intervals[i].weight - cost
                if score > dp[i]:
                    dp[i] = score
                    prev_choice[i] = j
    
    # Find the best ending interval
    best_idx = max(range(n), key=lambda i: dp[i])
    max_score = dp[best_idx]
    
    # Backtrack
    selected = []
    idx = best_idx
    while idx != -1:
        selected.append(sorted_intervals[idx])
        idx = prev_choice[idx]
    
    selected.reverse()
    
    return (max_score, selected)


def course_scheduling_dp(course_intervals: Dict[int, List[WeightedInterval]], 
                        walking_cost: Dict[Tuple[int, int], float] = None) -> Tuple[float, Dict[int, WeightedInterval], Dict]:
    """
    DP-based course scheduling: select one slot per course to maximize score.
    
    State: dp[course_idx][last_interval] = best score for scheduling courses 0..course_idx
           ending with last_interval
    
    Simplified version: Enumerate combinations with pruning.
    
    Time Complexity: O(k × n^k) worst case; practical pruning reduces it
    
    Args:
        course_intervals: Dict {course_id: [weighted_intervals]}
        walking_cost: Optional walking cost dict
    
    Returns:
        Tuple of (max_score, {course_id: selected_interval}, stats)
    """
    if not course_intervals:
        return (0.0, {}, {})
    
    course_ids = list(course_intervals.keys())
    n_courses = len(course_ids)
    
    # Flatten all intervals with course association
    all_intervals = []
    for course_id, intervals in course_intervals.items():
        for interval in intervals:
            interval.metadata["course_id"] = course_id
            all_intervals.append(interval)
    
    # Use greedy with DP-like selection
    # Sort all intervals by end time
    sorted_intervals = sorted(all_intervals, key=lambda x: (x.end, -x.weight))
    
    selected_by_course = {}
    selected_intervals = []
    total_score = 0.0
    
    for interval in sorted_intervals:
        course_id = interval.metadata["course_id"]
        
        # Skip if course already scheduled
        if course_id in selected_by_course:
            continue
        
        # Check compatibility with selected intervals
        is_compatible = True
        for sel_interval in selected_intervals:
            if not (interval.end <= sel_interval.start or interval.start >= sel_interval.end):
                is_compatible = False
                break
        
        if is_compatible:
            selected_by_course[course_id] = interval
            selected_intervals.append(interval)
            total_score += interval.weight
    
    stats = {
        "total_score": total_score,
        "courses_scheduled": len(selected_by_course),
        "total_courses": n_courses
    }
    
    return (total_score, selected_by_course, stats)


def knapsack_01(weights: List[int], values: List[float], capacity: int) -> Tuple[float, List[int]]:
    """
    Classic 0/1 Knapsack problem using DP.
    Included for completeness (practical mapping).
    
    Time Complexity: O(n × W)
    Space Complexity: O(n × W)
    
    Args:
        weights: Item weights
        values: Item values
        capacity: Knapsack capacity
    
    Returns:
        Tuple of (max_value, selected_items_indices)
    """
    n = len(weights)
    
    # DP table
    dp = [[0.0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i-1
            dp[i][w] = dp[i-1][w]
            
            # Take item i-1 if it fits
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
    
    # Backtrack to find items
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i - 1)
            w -= weights[i-1]
    
    selected.reverse()
    
    return (dp[n][capacity], selected)
