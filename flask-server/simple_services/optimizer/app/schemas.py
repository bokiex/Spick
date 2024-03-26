from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScheduleItem(BaseModel):
    event_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    schedule_id: int

class CommonSlot(BaseModel):
    start: datetime
    end: datetime

class OptimizedScheduleDay(BaseModel):
    date: str
    common_slot: CommonSlot
    attending_users: List[int]
    non_attending_users: List[int]

class OptimizedSchedules(BaseModel):
    schedules: List[OptimizedScheduleDay]
