'use client';

import React, { useState } from 'react';
import { ScheduleResult } from '@/lib/types';
import { apiMethods } from '@/lib/api';

export default function TimetablePage() {
  const [schedule, setSchedule] = useState<ScheduleResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [numCourses, setNumCourses] = useState(6);
  const [algorithm, setAlgorithm] = useState<'fast' | 'dp' | 'exact'>('fast');

  const generateSchedule = async () => {
    setLoading(true);
    setError(null);
    try {
      let result;
      const params = { num_courses: numCourses, algorithm, seed: 42 };

      if (algorithm === 'fast') {
        result = await apiMethods.scheduleFast(params);
      } else if (algorithm === 'dp') {
        result = await apiMethods.scheduleDP(params);
      } else {
        result = await apiMethods.scheduleExact(params);
      }

      setSchedule(result as ScheduleResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate schedule');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Timetable Optimizer</h1>

      {/* Controls */}
      <div className="bg-white p-6 rounded-lg shadow-md space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Number of Courses</label>
            <input
              type="number"
              min="1"
              max="12"
              value={numCourses}
              onChange={(e) => setNumCourses(Number(e.target.value))}
              className="w-full px-3 py-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Algorithm</label>
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value as 'fast' | 'dp' | 'exact')}
              className="w-full px-3 py-2 border rounded"
            >
              <option value="fast">Greedy (Fast)</option>
              <option value="dp">Dynamic Programming</option>
              <option value="exact">Exact (Branch & Bound)</option>
            </select>
          </div>
        </div>

        <div className="text-sm text-gray-600">
          <p><strong>Greedy:</strong> O(n log n) - Fastest, good quality</p>
          <p><strong>DP:</strong> O(n²) - Better quality, moderate speed</p>
          <p><strong>Exact:</strong> O(k^n) - Optimal solution, ≤10 courses recommended</p>
        </div>

        <button
          onClick={generateSchedule}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Generating...' : 'Generate Schedule'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {/* Schedule Result */}
      {schedule && (
        <div className="space-y-6">
          {/* Stats */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Schedule Statistics</h2>
            <div className="grid grid-cols-4 gap-4 text-sm">
              <div>
                <div className="text-gray-600">Courses Scheduled</div>
                <div className="text-2xl font-bold text-blue-600">{schedule.selected_slots.length}</div>
              </div>
              <div>
                <div className="text-gray-600">Total Preference</div>
                <div className="text-2xl font-bold text-green-600">{schedule.total_preference.toFixed(1)}</div>
              </div>
              <div>
                <div className="text-gray-600">Algorithm</div>
                <div className="text-lg font-semibold">{schedule.algorithm_used}</div>
              </div>
              <div>
                <div className="text-gray-600">Computation Time</div>
                <div className="text-lg font-semibold">{schedule.computation_time_ms.toFixed(2)} ms</div>
              </div>
            </div>
          </div>

          {/* Timetable Grid */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Weekly Timetable</h2>
            <TimetableGrid slots={schedule.selected_slots} />
          </div>

          {/* Course List */}
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Course Details</h2>
            <div className="space-y-2">
              {schedule.selected_slots.map((slot) => (
                <div key={slot.course_id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                  <div>
                    <div className="font-medium">{slot.course_name}</div>
                    <div className="text-sm text-gray-600">
                      {slot.day}, {formatTime(slot.start_min)} - {formatTime(slot.end_min)}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-600">Preference</div>
                    <div className="font-semibold text-green-600">{slot.preference_score.toFixed(1)}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function TimetableGrid({ slots }: { slots: any[] }) {
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  const hours = Array.from({ length: 9 }, (_, i) => i + 9); // 9 AM to 5 PM

  // Group slots by day and time
  const slotsByDayTime: Record<string, any> = {};
  slots.forEach((slot) => {
    const key = `${slot.day}-${slot.start_min}`;
    slotsByDayTime[key] = slot;
  });

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border-collapse border">
        <thead>
          <tr>
            <th className="border px-4 py-2 bg-gray-100">Time</th>
            {days.map((day) => (
              <th key={day} className="border px-4 py-2 bg-gray-100">{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {hours.map((hour) => (
            <tr key={hour}>
              <td className="border px-4 py-2 text-sm font-medium bg-gray-50">
                {formatTime(hour * 60)}
              </td>
              {days.map((day) => {
                const slot = slotsByDayTime[`${day}-${hour * 60}`];
                return (
                  <td key={day} className="border px-2 py-2 text-xs">
                    {slot ? (
                      <div className="bg-blue-100 p-2 rounded">
                        <div className="font-medium">{slot.course_name}</div>
                        <div className="text-gray-600">{slot.preference_score.toFixed(0)}</div>
                      </div>
                    ) : null}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function formatTime(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  const ampm = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours;
  return `${displayHours}:${mins.toString().padStart(2, '0')} ${ampm}`;
}
