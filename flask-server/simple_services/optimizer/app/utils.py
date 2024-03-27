from collections import defaultdict
from schemas import ScheduleItem, OptimizedScheduleDay, CommonSlot
from typing import List

def find_overlapping_times(schedules: List[ScheduleItem]) -> List[OptimizedScheduleDay]:
    schedules_by_day = defaultdict(list)
    for schedule in schedules:
        schedules_by_day[schedule.start_time.date()].append((schedule.start_time, schedule.end_time, schedule.user_id))

    optimized_schedule_days = []

    for day, day_schedules in schedules_by_day.items():
        day_schedules.sort(key=lambda x: (x[0], x[1]))
        time_blocks = []
        for start, end, user_id in day_schedules:
            time_blocks.append((start, 'start', user_id))
            time_blocks.append((end, 'end', user_id))
        time_blocks.sort()

        current_attendees = set()
        best_overlap = 0
        best_times = None
        for time, event, user_id in time_blocks:
            if event == 'start':
                current_attendees.add(user_id)
                if len(current_attendees) > best_overlap:
                    best_overlap = len(current_attendees)
                    best_times = (time, None)
            else:
                if len(current_attendees) == best_overlap and best_times[1] is None:
                    best_times = (best_times[0], time)
                current_attendees.remove(user_id)

        if best_times:
            attending_users = set()
            non_attending_users = set()
            for start, end, user_id in day_schedules:
                if start <= best_times[0] and end >= best_times[1]:
                    attending_users.add(user_id)
                else:
                    non_attending_users.add(user_id)

            optimized_schedule_days.append(
                OptimizedScheduleDay(
                    date=str(day),
                    common_slot=CommonSlot(start=best_times[0], end=best_times[1]),
                    attending_users=list(attending_users),
                    non_attending_users=list(non_attending_users),
                )
            )

    return optimized_schedule_days
