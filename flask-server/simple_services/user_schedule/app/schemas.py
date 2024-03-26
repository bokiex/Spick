# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserScheduleCreate(BaseModel):
    event_id: str
    user_id: int
    start_time: datetime
    end_time: datetime

class UserScheduleList(BaseModel):
    sched_list: List[UserScheduleCreate]
    
class ScheduleDeleteResponse(BaseModel):
    message: str

class UserScheduleInDB(UserScheduleCreate):
    schedule_id: int

    class Config:
        orm_mode = True

