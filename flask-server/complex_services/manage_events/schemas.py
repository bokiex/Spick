from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import UploadFile, File

class Recommend(BaseModel):
    user_id: int
    event_name: str
    event_desc: str
    image: str
    datetime_start: datetime
    datetime_end: datetime
    type: str
    township: str
    time_out: datetime
    invitees: list

class Event(BaseModel):
    user_id: int
    start_time: datetime
    end_time: datetime
    recommendation: list
