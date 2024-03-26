from collections import defaultdict
from typing import List
from schemas import ScheduleItem, OptimizedScheduleDay, CommonSlot

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

        max_attendees = 0
        current_attendees = set()
        potential_slots = []
        slot_start = None

        for time, event, user_id in time_blocks:
            if event == 'start':
                if not current_attendees:  # if starting a new slot
                    slot_start = time
                current_attendees.add(user_id)
            else:
                current_attendees.remove(user_id)
                if not current_attendees:  # if ending a slot
                    potential_slots.append((slot_start, time, max_attendees))
                    slot_start = None
                    max_attendees = max(max_attendees, len(current_attendees))
        
        # Filtering slots that have the max number of attendees
        slots_with_max_attendees = [slot for slot in potential_slots if slot[2] == max_attendees]

        for slot_start, slot_end, _ in slots_with_max_attendees:
            attending_users = set()
            non_attending_users = set()
            for start, end, user_id in day_schedules:
                if start <= slot_start and end >= slot_end:
                    attending_users.add(user_id)
                else:
                    non_attending_users.add(user_id)

            optimized_schedule_days.append(
                OptimizedScheduleDay(
                    date=str(day),
                    common_slot=CommonSlot(start=slot_start, end=slot_end),
                    attending_users=list(attending_users),
                    non_attending_users=list(non_attending_users),
                )
            )

    return optimized_schedule_days
