from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScheduleItem(BaseModel):
    event_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    schedule_id: int

class ScheduleList(BaseModel):
    sched_list: List[ScheduleItem]

class CommonSlot(BaseModel):
    start: datetime
    end: Optional[datetime] = None

class OptimizedScheduleDay(BaseModel):
    date: str
    common_slot: CommonSlot
    attending_users: List[int]  # Adjusted to reflect the user_id type
    non_attending_users: List[int]  # Adjusted to reflect the user_id type

class OptimizedSchedules(BaseModel):
    schedules: List[OptimizedScheduleDay]
