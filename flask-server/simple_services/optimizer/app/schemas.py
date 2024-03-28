from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScheduleItem(BaseModel):
    event_id: str
    user_id: int
    start_time: datetime
    end_time: datetime
    schedule_id: int

class CommonSlot(BaseModel): #no longer need this
    start: datetime
    end: datetime

class OptimizedScheduleDay(BaseModel):
    event_id: str
    date: str
    start: datetime
    end: datetime
    attending_users: List[int]
    non_attending_users: List[int]

class OptimizedSchedules(BaseModel):
    schedules: List[OptimizedScheduleDay]
