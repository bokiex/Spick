from fastapi import FastAPI
from typing import List, Dict
from datetime import datetime
from collections import defaultdict
from schemas import OptimizedScheduleDay, OptimizedSchedules, ScheduleItem, CommonSlot

app = FastAPI()

@app.post('/optimize_schedule', response_model=OptimizedSchedules)
def optimize_schedule(schedule_list: List[ScheduleItem]):
    schedules_by_day: Dict[datetime, List] = defaultdict(list)
    for schedule in schedule_list:
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
                if not current_attendees and slot_start:  # if ending a slot
                    potential_slots.append((slot_start, time, len(current_attendees)))
                    slot_start = None
        
        # Filtering slots that have the max number of attendees
        slots_with_max_attendees = [slot for slot in potential_slots if slot[2] == max(max_attendees, len(current_attendees))]

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

    return OptimizedSchedules(schedules=optimized_schedule_days)


#Input
# [
#     {
#         "event_id": 1,
#         "user_id": 101,
#         "start_time": "2024-04-01T09:00:00",
#         "end_time": "2024-04-01T10:00:00",
#         "schedule_id": 1
#     },
#     {
#         "event_id": 1,
#         "user_id": 102,
#         "start_time": "2024-04-01T09:00:00",
#         "end_time": "2024-04-01T10:00:00",
#         "schedule_id": 1
#     },
#     {
#         "event_id": 1,
#         "user_id": 103,
#         "start_time": "2024-04-01T22:00:00",
#         "end_time": "2024-04-01T23:00:00",
#         "schedule_id": 1
#     },
#     {
#         "event_id": 2,
#         "user_id": 104,
#         "start_time": "2024-04-01T22:00:00",
#         "end_time": "2024-04-01T23:00:00",
#         "schedule_id": 1
#     },
#     {
#         "event_id": 1,
#         "user_id": 105,
#         "start_time": "2024-04-02T10:00:00",
#         "end_time": "2024-04-02T22:30:00",
#         "schedule_id": 1
#     }
# ]
"""
Output
{
    "schedules": [
        {
            "date": "2024-04-01",
            "common_slot": {
                "start": "2024-04-01T09:00:00",
                "end": "2024-04-01T10:00:00"
            },
            "attending_users": [
                101,
                102
            ],
            "non_attending_users": [
                104,
                103
            ]
        },
        {
            "date": "2024-04-01",
            "common_slot": {
                "start": "2024-04-01T22:00:00",
                "end": "2024-04-01T23:00:00"
            },
            "attending_users": [
                104,
                103
            ],
            "non_attending_users": [
                101,
                102
            ]
        },
        {
            "date": "2024-04-02",
            "common_slot": {
                "start": "2024-04-02T10:00:00",
                "end": "2024-04-02T22:30:00"
            },
            "attending_users": [
                105
            ],
            "non_attending_users": []
        }
    ]
}
"""