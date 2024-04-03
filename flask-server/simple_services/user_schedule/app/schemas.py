# schemas.py
from pydantic import BaseModel
from typing import List

class UserScheduleCreate(BaseModel):
    event_id: str
    user_id: int
    start_time: str
    end_time: str

class UserScheduleInDB(UserScheduleCreate):
    schedule_id: int

class UserScheduleList(BaseModel):
    sched_list: List[UserScheduleInDB]

class intake(BaseModel):
        sched_list: List[UserScheduleCreate]