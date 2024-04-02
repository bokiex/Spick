from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScheduleItem(BaseModel):
    event_id: str
    user_id: int
    start_time: str
    end_time: str
    schedule_id: int

class CommonSlot(BaseModel): #no longer need this
    start: str
    end: str

class OptimizedScheduleDay(BaseModel):
    event_id: str
    date: str
    start: str
    end: str
    attending_users: List[int]
    non_attending_users: List[int]

class OptimizedSchedules(BaseModel):
    schedules: List[OptimizedScheduleDay]
