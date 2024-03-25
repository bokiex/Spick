from fastapi import FastAPI
from typing import List
from schemas import ScheduleItem, OptimizedSchedules
from utils import find_overlapping_times

app = FastAPI()

@app.post('/optimize_schedule', response_model=OptimizedSchedules)
async def optimize_schedule(schedule_list: List[ScheduleItem]):
    optimized_schedule_days = find_overlapping_times(schedule_list)
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