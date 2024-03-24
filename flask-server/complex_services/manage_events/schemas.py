from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Recommend(BaseModel):
    user_id: int
    event_name: str
    event_desc: str
    datetime_start: datetime
    datetime_end: datetime
    type: str
    township: str
    time_out: datetime

class Event(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime
    recommendation: list
