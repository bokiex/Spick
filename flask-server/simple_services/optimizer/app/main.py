from fastapi import FastAPI
from typing import List, Dict
from datetime import datetime
from collections import defaultdict
from schemas import OptimizedScheduleDay, OptimizedSchedules, ScheduleItem, CommonSlot
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
    return JSONResponse(status_code=200, content={"message": "Optimizer is online."})

@app.post('/optimize_schedule', response_model=OptimizedSchedules)
def optimize_schedule(schedule_list: List[ScheduleItem]):
    optimized_schedules = []
    schedules_by_day = defaultdict(lambda: defaultdict(list))

    # Step 1: Organize schedules by event and then by day using datetime for processing
    for schedule in schedule_list:
        start_datetime = datetime.fromisoformat(schedule.start_time)  # Convert to datetime
        end_datetime = datetime.fromisoformat(schedule.end_time)  # Convert to datetime
        day_key = start_datetime.date()
        
        # Append the original schedule object; datetime objects are used for logic only
        schedules_by_day[schedule.event_id][day_key].append((schedule, start_datetime, end_datetime))

    # Step 2: Processing logic and building the optimized schedules
    for event_id, schedules_per_day in schedules_by_day.items():
        for day, day_schedules in schedules_per_day.items():
            # Use the datetime objects for sorting and logic
            time_blocks = [(start_dt, 1, sch.user_id) for sch, start_dt, end_dt in day_schedules] + \
                          [(end_dt, -1, sch.user_id) for sch, start_dt, end_dt in day_schedules]
            time_blocks.sort()
            current_users = set()
            max_overlap_users = set()
            max_attendees = 0
            start_overlap = None

            for time, action, user_id in time_blocks:
                if action == 1:  # Start of an event
                    current_users.add(user_id)
                    if len(current_users) > max_attendees:
                        max_attendees = len(current_users)
                        max_overlap_users = current_users.copy()
                        start_overlap = time
                else:  # End of an event
                    current_users.remove(user_id)

            if max_overlap_users:
                # Finding the minimum end time for the max overlap period
                end_overlap = min(end_dt for _, start_dt, end_dt in day_schedules if start_dt <= start_overlap and _.user_id in max_overlap_users)
                non_attendees = [sch.user_id for sch, _, _ in day_schedules if sch.user_id not in max_overlap_users]

                optimized_schedules.append(OptimizedScheduleDay(
                    event_id=event_id,
                    date=day.isoformat(),  # Convert day back to string
                    start=start_overlap.isoformat(),  # Convert datetime to ISO format string
                    end=end_overlap.isoformat(),  # Convert datetime to ISO format string
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