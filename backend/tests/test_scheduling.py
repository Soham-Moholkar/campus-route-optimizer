"""
Unit tests for scheduling algorithms.
"""
import pytest
from app.algorithms.greedy.activity_selection import Activity, greedy_activity_selection_by_finish
from app.algorithms.dp.weighted_interval import WeightedInterval, weighted_interval_scheduling_dp


def test_greedy_activity_selection():
    """Test greedy activity selection."""
    activities = [
        Activity(id=0, start=1, end=4, score=1),
        Activity(id=1, start=3, end=5, score=1),
        Activity(id=2, start=0, end=6, score=1),
        Activity(id=3, start=5, end=7, score=1),
        Activity(id=4, start=8, end=9, score=1),
        Activity(id=5, start=5, end=9, score=1)
    ]
    
    selected = greedy_activity_selection_by_finish(activities)
    
    # Should select activities with earliest finish times
    assert len(selected) >= 2
    # First selected should be one with earliest finish time
    assert selected[0].id == 0  # ends at 4


def test_weighted_interval_scheduling():
    """Test DP weighted interval scheduling."""
    intervals = [
        WeightedInterval(id=0, start=1, end=4, weight=5),
        WeightedInterval(id=1, start=3, end=5, weight=1),
        WeightedInterval(id=2, start=0, end=6, weight=8),
        WeightedInterval(id=3, start=5, end=7, weight=4),
        WeightedInterval(id=4, start=8, end=9, weight=3),
    ]
    
    max_weight, selected = weighted_interval_scheduling_dp(intervals)
    
    # Optimal solution
    assert max_weight >= 8  # At least the single interval with weight 8


def test_activity_overlap():
    """Test activity overlap detection."""
    act1 = Activity(id=0, start=1, end=5, score=1)
    act2 = Activity(id=1, start=4, end=8, score=1)
    act3 = Activity(id=2, start=6, end=9, score=1)
    
    assert act1.overlaps(act2) == True
    assert act2.overlaps(act3) == True
    assert act1.overlaps(act3) == False


def test_weighted_interval_empty():
    """Test weighted interval scheduling with empty input."""
    max_weight, selected = weighted_interval_scheduling_dp([])
    
    assert max_weight == 0.0
    assert len(selected) == 0


def test_weighted_interval_single():
    """Test weighted interval scheduling with single interval."""
    intervals = [WeightedInterval(id=0, start=1, end=4, weight=10)]
    
    max_weight, selected = weighted_interval_scheduling_dp(intervals)
    
    assert max_weight == 10.0
    assert len(selected) == 1
