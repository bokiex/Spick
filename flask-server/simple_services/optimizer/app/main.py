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
    optimized_schedules = []
    schedules_by_day = defaultdict(lambda: defaultdict(list))

    # Organize schedules by event and then by day
    for schedule in schedule_list:
        day_key = schedule.start_time.date()
        schedules_by_day[schedule.event_id][day_key].append(schedule)

    for event_id, schedules_per_day in schedules_by_day.items():
        for day, day_schedules in schedules_per_day.items():
            time_blocks = [(s.start_time, 1, s.user_id) for s in day_schedules] + [(s.end_time, -1, s.user_id) for s in day_schedules]
            time_blocks.sort()
            current_users = set()
            max_overlap_users = set()
            max_attendees = 0
            start_overlap = None

            for time, action, user_id in time_blocks:
                if action == 1:  # start
                    current_users.add(user_id)
                    if len(current_users) > max_attendees:
                        max_attendees = len(current_users)
                        max_overlap_users = current_users.copy()
                        start_overlap = time
                else:
                    current_users.remove(user_id)

            if max_overlap_users:
                end_overlap = min(s.end_time for s in day_schedules if s.user_id in max_overlap_users and s.start_time <= start_overlap)
                non_attendees = [s.user_id for s in day_schedules if s.user_id not in max_overlap_users]

                optimized_schedules.append(OptimizedScheduleDay(
                    event_id=event_id,
                    date=str(day),
                    start=start_overlap,
                    end=end_overlap,
                    attending_users=list(max_overlap_users),
                    non_attending_users=non_attendees
                ))

    return OptimizedSchedules(schedules=optimized_schedules)

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