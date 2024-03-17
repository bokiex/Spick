from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    event_name: str
    event_desc: str
    start_time: datetime
    end_time: datetime
    timeout: datetime
    user_id: int

class Invitee(BaseModel):
    event_id: int
    user_id: int
    status: str