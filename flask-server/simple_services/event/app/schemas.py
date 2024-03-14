from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    event_id: int
    event_name: str
    start_time: datetime
    end_time: datetime
    event_location: str
