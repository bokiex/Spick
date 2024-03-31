from fastapi import FastAPI
from typing import List, Dict
from datetime import datetime
from collections import defaultdict
from schemas import OptimizedScheduleDay, OptimizedSchedules, ScheduleItem, CommonSlot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/online")
def online():
    return {"message": "Optimizer is online."}

@app.post('/optimize_schedule', response_model=OptimizedSchedules)
def optimize_schedule(schedule_list: List[ScheduleItem]):
    schedules_by_day: Dict[datetime, List] = defaultdict(list)
    for schedule in schedule_list:
        schedules_by_day[schedule.start_time.date()].append((schedule.start_time, schedule.end_time, schedule.user_id))
        id = schedule.event_id

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
                    event_id = id,
                    date=str(day),
                    start=slot_start,
                    end=slot_end,
                    attending_users=list(attending_users),
                    non_attending_users=list(non_attending_users),
                )
            )
    max_attendees_count = max(len(day.attending_users) for day in optimized_schedule_days)
    filtered_schedule_days = [day for day in optimized_schedule_days if len(day.attending_users) == max_attendees_count]



    return OptimizedSchedules(schedules=filtered_schedule_days)


# Input
"""
[
    {
        "schedule_id": 1,
        "event_id": "123123",
        "user_id": 101,
        "start_time": "2024-04-01T11:00:00",
        "end_time": "2024-04-01T12:00:00"
    }
]
"""
# Output
"""
{
    "schedules": [
        {
            "event_id": "123123",
            "date": "2024-04-01",
            "start": "2024-04-01T11:00:00",
            "end": "2024-04-01T12:00:00",
            "attending_users": [
                101
            ],
            "non_attending_users": []
        }
    ]
}
"""