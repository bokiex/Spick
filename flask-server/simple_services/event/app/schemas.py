from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    event_id: int
    event_name: str
    event_desc: str
    start_time: datetime
    end_time: datetime
    timeout: datetime
    event_location: str
    user_id: int

