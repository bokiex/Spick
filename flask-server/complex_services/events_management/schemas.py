from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Recommend(BaseModel):
    user_id: int
    event_name: str
    event_desc: str
    start_time: datetime
    end_time: datetime
    search: dict
    time_out: datetime

class Event(BaseModel):
    user_id: int
    event_id: int
    start_time: datetime
    end_time: datetime
    recommendation: list
